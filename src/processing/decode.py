import cv2
import numpy as np
# import matplotlib.pyplot as plt
import os
from pathlib import Path
import sys


def save_binary(data, filename):
	"""saves a binary sequence to file
	
	inputs:
	 - data: numpy.ndarray, shape: (N,), dtype: int
	 - filename: path to file
	"""
	reconstr_data = []
	for bit_array in data.reshape(-1,8):
		byte_str = ''.join([str(bit) for bit in bit_array])
		i = int(byte_str,2)
		reconstr_data.append(i)

	with open(filename, 'wb') as f:
		f.write(bytes(reconstr_data))

def frame_to_bin_mask(frame_masked):
	"""
	"""
	mask = (frame_masked > 127).astype(float)
	return mask

def reduce_masks(candidates, patch_height=8, patch_width=8):
	"""takes a list of masks and "restores" the binary sequence 

	input:
	 - candidates: list of (HEIGHT,WIDTH,3) numpy arrays, type: int
	"""

	if candidates == []:
		return []

	h,w,c = candidates[0].shape
	mask_h = h // patch_height
	mask_w = w // patch_width
	rep = len(candidates)

	#concatenate them along the color channel:
	#concat -> (h,w,c*rep)
	bin_seq = np.concatenate(candidates,axis=-1)\
		.reshape(mask_h, patch_height, mask_w, patch_width, c*rep)\
		.swapaxes(1,2)\
		.reshape(mask_h*mask_w, patch_height*patch_width*c*rep)\
		.mean(axis=-1)
	bin_seq = (1.999*bin_seq).astype(int)
	return bin_seq


def restore_from_video(
		video_path,
		out_path,
		tail_size,
		patch_height = 8,
		patch_width = 8,
		rep = 10
	):

	cap = cv2.VideoCapture(video_path)
	width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

	seq_len = height//patch_height*width//patch_width
	candidates = []
	bin_seq_reconstructed = []
	counter = 0

	the_end = False

	while True:

		if counter % rep == 0 or the_end:
			bin_seq = reduce_masks(candidates,patch_height,patch_width)
			bin_seq_reconstructed += list(bin_seq)
			candidates = []

			if the_end:
				break

		ret, frame_masked = cap.read()
		if not ret:
			the_end = True
			continue

		mask_enlarged = frame_to_bin_mask(frame_masked)
		candidates.append(mask_enlarged)
		counter += 1

	cap.release()

	bin_seq_reconstructed = np.array(bin_seq_reconstructed[:-tail_size])
	save_binary(bin_seq_reconstructed, out_path)





def main():
	import argparse
	parser = argparse.ArgumentParser()

	parser.add_argument(
		'--video_path',
		'-v',
		help='video which contains the file'
	)
	parser.add_argument(
		'--out_path',
		'-o',
		help='restored file path'
	)
	parser.add_argument(
		'--tail_size',
		'-t',
		help='number of filler bits at the end',
		type=int
	)
	parser.add_argument(
		'--patch_height',
		'-p_h',
		help='',
		type=int,
		default=8
	)
	parser.add_argument(
		'--patch_width',
		'-p_w',
		help='',
		type=int,
		default=8
	)
	parser.add_argument(
		'--repetitions',
		'-r',
		help='',
		type=int,
		default=10
	)
	args = parser.parse_args()

	restore_from_video(
		video_path = args.video_path,
		out_path = args.out_path,
		tail_size = args.tail_size,
		patch_height = args.patch_height,
		patch_width = args.patch_width,
		rep = args.repetitions
	)


if __name__ == '__main__':
	main()