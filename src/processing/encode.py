from pathlib import Path
import numpy as np
import cv2
import os
import shutil
import sys
import json


def get_binary(filename):
	"""returns the binary of file provided by a path
	
	output: numpy.ndarray, shape: (N,)
	"""

	with open(filename, 'rb') as f:
		data = f.read()

	data = [format(c, '08b') for c in data]
	data = list(''.join(data))
	data = np.asarray([int(bit) for bit in data])
	return data

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


def get_bin_mask(
		bin_segment,
		frame_shape,
		patch_height,
		patch_width
	):

	h, w, c = frame_shape
	mask_w = w // patch_width
	mask_h = h // patch_height

	bin_mask = bin_segment[...,None].repeat(patch_height*patch_width,axis=-1)
	bin_mask = bin_mask.reshape(mask_h, mask_w, patch_height, patch_width)
	bin_mask = bin_mask.swapaxes(1,2).reshape(h,w)
	bin_mask = bin_mask[...,None].repeat(3,axis=-1)

	return bin_mask

def get_correct_segment(
		bin_seq,
		frame_shape,
		frame_idx,
		patch_height,
		patch_width,
		rep
	):
	h, w, c = frame_shape
	bit_count = w * h // (patch_height*patch_width)
	return bin_seq[frame_idx//rep*bit_count:(frame_idx//rep+1)*bit_count]

def encode_in_frame(
		bin_mask,
		frame
	):

	frame_masked = frame.copy() // 2
	frame_masked[bin_mask == 1] += 128

	return frame_masked

def encode_in_video(
		video_path,
		filename,
		settings_file,
		out_video,
		temp_path = 'tmp',
		patch_height = 8,
		patch_width = 8,
		rep = 10
	):
	"""saves a new video

	inputs:
	 - video_path: path to base video
	 - bin_seq: the whole binary sequence of the file
	 - patch_size:
	 - out_path: the saved video
	 - rep: the number of consecutive frames that should have the save mask
	output:
	"""
	settings_dict = {}

	if not os.path.exists(temp_path):
		os.mkdir(temp_path)

	cap = cv2.VideoCapture(str(video_path))

	w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	c = 3
	frame_shape = (h, w, c)
	fps = int(cap.get(cv2.CAP_PROP_FPS))

	bin_seq = get_binary(filename)

	#split the bin_seq into fitting and tail:
	bits_per_frame = h * w // (patch_height*patch_width)
	tail_len = len(bin_seq) % bits_per_frame
	overflow = bits_per_frame - tail_len
	bin_seq = np.concatenate([bin_seq,np.zeros(overflow,dtype=int)])
	frames_needed = rep * len(bin_seq) // bits_per_frame
	frames_total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

	settings_dict['overflow'] = overflow
	settings_dict['patch_width'] = patch_width
	settings_dict['patch_height'] = patch_height
	settings_dict['rep'] = rep
	
	# print('frames needed:',frames_needed)
	# print('frame count:',frames_total)
	# print()

	frame_idx = 0
	while frame_idx < frames_needed:

		if frame_idx % frames_total == 0:
			#we arrived at the end of the video, restart it
			#(later maybe start it from the end)
			cap.release()
			cap = cv2.VideoCapture(str(video_path))

		#we create a new binary mask every 'rep' turns:
		if frame_idx % rep == 0:
			bin_segment = get_correct_segment(
				bin_seq,
				frame_shape,
				frame_idx,
				patch_height,
				patch_width,
				rep
			)
			# print(bin_segment.shape)
			# print(frame_idx)
			# print()
			bin_mask = get_bin_mask(
				bin_segment,
				frame_shape,
				patch_height,
				patch_width
			)

			# if frame_idx % (10*rep) == 0:
			# 	print(f'{bits_per_frame*frame_idx//rep}/{len(bin_seq)} bits processed')

		ret, frame = cap.read()
		frame = frame.astype(int)

		frame_masked = encode_in_frame(
			bin_mask,
			frame
		)

		cv2.imwrite(f'{temp_path}/_masked_{frame_idx:06}.png',frame_masked.astype(np.uint8))
		frame_idx += 1

	cap.release()
	os.system(f'ffmpeg -framerate {fps} -i {temp_path}/_masked_%06d.png -c:v copy {out_video}')
	shutil.rmtree(temp_path)

	#save the settings:
	with open(settings_file,'w') as f:
		json.dump(settings_dict,f)




def main():
	import argparse
	
	parser = argparse.ArgumentParser()
	parser.add_argument(
		'--filename',
		'-f',
		help='file to be encoded'
	)
	parser.add_argument(
		'--out_video',
		'-o',
		help='path of the output video to be created'
	)
	parser.add_argument(
		'--base_video',
		'-v',
		help='video to write the file onto'
	)
	parser.add_argument(
		'--temp_path',
		'-t',
		default='tmp'
	)
	parser.add_argument(
		'--settings_file',
		'-s',
		help='json to store info in (patch dimensions, tail length etc)'
	)
	parser.add_argument(
		'--repetitions',
		'-r',
		type=int,
		default=10,
		help='the number of consecutive frames that have the same mask'
	)
	parser.add_argument(
		'--patch_height',
		'-p_h',
		type=int,
		default=8
	)
	parser.add_argument(
		'--patch_width',
		'-p_w',
		type=int,
		default=8
	)
	args = parser.parse_args()

	#patch_size = 8

	encode_in_video(
		video_path = args.base_video,
		filename = args.filename,
		settings_file = args.settings_file,
		temp_path = args.temp_path,
		patch_height = args.patch_height,
		patch_width = args.patch_width,
		out_video = args.out_video,
		rep=args.repetitions
	)




if __name__ == '__main__':
	main()