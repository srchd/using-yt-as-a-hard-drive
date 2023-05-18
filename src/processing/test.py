import os
import sys
from pathlib import Path
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math
import pickle as pkl

from .utils import get_binary_string, binary_to_file

def _encode_in_video(
		binary_string,
		frame,
		idx,
		patch_size=8
	):
	"""
	idea: we can change frame but not change frame_idx so consequent frames
	would still have the same binary mask, evading potential data loss
	due to youtube's conversion

	NOTES:
	 - frame pixels are integer values
	"""
	h, w, c = frame.shape
	mask_w = w // patch_size
	mask_h = h // patch_size

	bit_count = mask_w * mask_h
	target = binary_string[idx*bit_count:(idx+1)*bit_count]

	bin_mask = target[...,None].repeat(patch_size**2,axis=-1)
	bin_mask = bin_mask.reshape(mask_h, mask_w, patch_size, patch_size)
	bin_mask = bin_mask.swapaxes(1,2).reshape(h,w)
	bin_mask = bin_mask[...,None].repeat(3,axis=-1)

	frame_masked = frame.copy() // 2 #[0,255] -> [0,127]
	#what we want: 0s should be in [0,127], 1s in [128,255]
	#that way we can transform it back to [-255,255] so we can do
	#element-wise division - > -1 is 0, 1 is 1
	# print(frame_masked.min(),frame_masked.max())

	frame_masked[bin_mask == 1] += 128
	# print(frame_masked[bin_mask == 1].min(),frame_masked[bin_mask == 1].max())
	# print(frame_masked[bin_mask == 0].min(),frame_masked[bin_mask == 0].max())

	return frame_masked

def _encode_in_video_multirange(
		binary_string,
		frame,
		idx,
		range_num=4,
		patch_size=8
	):
	"""
	
	We take a segment of the input binary sequence and encode it into the
	current frame.
	How do we select the right length of the binary seq?
	We would like to divide the original range [0..255] into N segments
	Since we can't know for sure how close together the pixel values will
	be, for now we'll be content with just pushing them to a single
	sub-range.
	N can represent logN bit seqs, so ideally it should be a power of 2
	So if N=4, possible binary strings are: 00, 01, 10, 11

	SPECULATION:
	 - if we add random uniform noise to patches and make them bigger
	 (maybe 10x10, 16x16, 20x20) we could separate them into several intervals
	 This way we could represent bit seqs directly.
	 Problem with this: if the values are too close together, separation
	 might become harder, especially if youtube's algo messes it up
	 (local ordering of pixel values that are close together might change)
	 Potential solution: N changes across patches depending on how well we
	 can divide them

	NOTES:
	 - frame pixels are integer values, [0..255]
	"""
	h, w, c = frame.shape
	mask_w = w // patch_size
	mask_h = h // patch_size

	#subseq_size == 2 if range_num == 4
	subseq_size = int(math.log(range_num,2)) #possible binary strings encoded into a single pixel

	bit_count = mask_h * mask_w * c * subseq_size
	target_bin = binary_string[idx*bit_count:(idx+1)*bit_count]

	target_bin = target_bin.reshape(mask_h, mask_w, c, subseq_size)
	target_dec = np.zeros(target_bin.shape[:-1]) #we leave subseq_size out
	for i in range(subseq_size):
		target_dec += (2**i)*target_bin[...,i]

	#should we work with floats for now, and convert at the end?
	step_size = 255 / range_num

	#target shape: (mask_h, mask_w, 3) -> (h, w, 3)
	#enlarge by patch_size
	mask_dec = target_dec[:,:,None,:].repeat(patch_size**2,axis=-2)
	mask_dec = mask_dec.reshape(mask_h, mask_w, patch_size, patch_size, c)
	mask_dec = mask_dec.swapaxes(1,2).reshape(h,w,c)
	#mask_dec basically contains the offset of the interval,
	#	so we just need to translate pixel values but that amount * step_size

	frame_masked = frame.copy() / range_num
	frame_masked += (step_size * mask_dec)

	return frame_masked.astype(int)


def frame_to_bin_mask(frame_masked):
	"""
	"""
	mask = (frame_masked > 127).astype(float)
	return mask


def shrink_mask(enlarged_mask, patch_size=8):
	"""the challenge is correctly shrinking the mask.
	With yt's conversion we don't know what to expect
	"""
	h, w, c = enlarged_mask.shape
	mask_h = h // patch_size
	mask_w = w // patch_size
	mask = enlarged_mask\
		.reshape(mask_h, patch_size, mask_w, patch_size, c)\
		.swapaxes(1,2)\
		.reshape(mask_h, mask_w, patch_size**2, c)\
		.mean(axis=-2)
	return mask


def round_mask(mask):
	"""shrunk mask might include values between 0 and 1. Make them either 0 or 1
	"""
	# _mask = mask.copy()
	_mask = mask.mean(axis=-1)
	_mask[_mask<0.5] = 0.0
	_mask[_mask>=0.5] = 1.0
	return _mask.astype(int)

def inspect_masked_frame(
		masked,
		patch_size=8,
		range_num=4
	):

	h, w, c = masked.shape
	mask_w = w // patch_size
	mask_h = h // patch_size
	row = masked[0:patch_size,:,:] #(patch_size, patch_size*mask_w, c)
	row.swapaxes(0,1).reshape(mask_w, patch_size**2, c)


if __name__ == '__main__':

	video_name = 'rick.mp4'
	file_name = '08.pdf'
	reconstructed_file_name = '08_reconstr.pdf'

	input_path = Path(__file__).parent.parent.parent

	video_path = input_path / video_name
	file_path = input_path / file_name

	bin_str = get_binary_string(file_path)
	bin_seq = (np.asarray(bin_str) == '1').astype(int)

	cap = cv2.VideoCapture(str(video_path))
	#writer = cv2.VideoWriter()

	idx = 0
	mask_rep = 10 #how many consecutive frames should have the same mask
	# begin = 20

	#print(cap.get(cv2.CAP_PROP_FPS))
	#let's say we hardcode these:
	WIDTH = 640
	HEIGHT = 360
	PATCH_SIZE = 8

	mask_width = WIDTH // PATCH_SIZE
	mask_height = HEIGHT // PATCH_SIZE
	bits_per_frame = mask_width * mask_height
	bits_total = len(bin_seq)
	frames_full = bits_total // bits_per_frame
	bits_leftover = bits_total % bits_per_frame

	# how this is calculated:
	# frames_full is the the number of frames where the bits
	#   fit perfectly
	# +1 because of the 'tail' of the bit sequence (the rest will be
	#   filled with 0s)
	# mask_rep: how many consecutive frames should have the same bin mask
	frames_needed = (frames_full + 1) * mask_rep

	reconstructed_seq = []

	prev_seq = np.zeros(bits_per_frame).astype(int)
	# print('bits per frame:',bits_per_frame)

	print('frames needed:',frames_needed)

	seqs_added = 0

	frames = []

	# while idx < frames_needed - 1:
	while idx < 10:
		# break
		ret, frame = cap.read()
		# w, h, c = frame.shape


		# if idx < begin:
		# 	idx += 1
		# 	continue
		# fig, axs = plt.subplots(2,2)
		frame = frame.astype(int)
		# print('frame:',frame.shape)
		# frame_masked = _encode_in_video_multirange(
		# 	binary_string=bin_seq,
		# 	frame=frame,
		# 	idx=(idx)//mask_rep,
		# 	range_num=4,
		# 	patch_size=8
		# )

		frame_masked = _encode_in_video(
			binary_string=bin_seq,
			frame=frame,
			idx=idx//mask_rep,
			patch_size=PATCH_SIZE
		)
		idx += 1

		frames.append(frame_masked)
		continue
		# print('frame_masked:',frame_masked.shape)

		# plt.figure()
		# plt.imshow(frame_masked[...,::-1])
		# plt.show()


		# break

		enlarged_mask = frame_to_bin_mask(frame_masked)
		mask = shrink_mask(enlarged_mask)
		mask = round_mask(mask)
		#rounded mask should be 2D now

		mask_seq = mask.reshape(-1)
		# print(mask_seq.shape)
		# print(prev_seq.shape)
		if (mask_seq == prev_seq).sum() != 0:
			seqs_added += 1
			reconstructed_seq += list(mask_seq)
			prev_seq = mask_seq

		# if seqs_added % 50 == 0:
		# 	print(f'different seqs: {seqs_added}/{frames_full}, total: {idx}/{frames_needed}')

		# axs[0,0].imshow(frame[...,::-1])
		# axs[0,0].set_title('original frame')
		# axs[0,1].imshow(frame_masked[...,::-1])
		# axs[0,1].set_title('masked frame')
		# axs[1,0].imshow(enlarged_mask)
		# axs[1,0].set_title('mask from masked frame')
		# axs[1,1].imshow(mask*255)
		# axs[1,1].set_title('reduced mask (pixel = bit)')
		# plt.show()
		# break

		# if cv2.waitKey(1) & 0xFF == ord('q'):
		# 	break

	#read the last frame and add the tail:

	with open('asd.pkl','wb') as f:
		pkl.dump(frames,f)

	sys.exit(0)

	ret, frame = cap.read()
	frame = frame.astype(int)
	frame_masked = _encode_in_video(
		binary_string=np.asarray(list(bin_seq)+[0 for _ in range(bits_per_frame-bits_leftover)]),
		frame=frame,
		idx=idx//mask_rep,
		patch_size=PATCH_SIZE
	)
	enlarged_mask = frame_to_bin_mask(frame_masked)
	mask = shrink_mask(enlarged_mask)
	mask = round_mask(mask)

	reconstructed_seq += list(mask.reshape(-1)[:bits_leftover])
	reconstructed_seq = np.asarray(reconstructed_seq)

	binary_to_file(reconstructed_seq, input_path/reconstructed_file_name)

	cap.release()
	cv2.destroyAllWindows()