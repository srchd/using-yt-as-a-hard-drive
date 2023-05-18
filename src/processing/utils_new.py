import cv2
import numpy as np
import matplotlib.pyplot as plt


def display_data(data: list, size: tuple):
	"""converts a binary string to a 4d numpy array
	(frame index, height, width, color channel)
	also adds a tail make the array complete
	and returns the tail's length

	size: height, width
	"""
	
	height, width = size
	tail = width*height - len(data) % (width*height)
	data += '0' * tail
	length = len(data)
	frame_num = length // (width*height)
	data = np.asarray(data) == '1'
	data = data.reshape(frame_num,height,width,1).repeat(3,axis=-1).astype(np.uint8)*255

	return data, tail

def get_binary_string(filename):
	with open(filename, 'r', encoding='ISO-8859-1') as f:
		data = f.read()

	data = [format(ord(c), '08b') for c in data]
	data = list(''.join(data))

	return data

def generate_video(path, data, codec='DIVX', fps=24):
	
	shape = data.shape
	assert path.split('.')[-1] == 'avi'
	assert len(shape) == 4
	assert shape[-1] == 3

	height, width = shape[1:-1]
	out = cv2.VideoWriter(path, cv2.VideoWriter_fourcc(*codec), fps, (width, height))

	for i, frame in enumerate(data):
		out.write(frame)
	out.release()


if __name__ == '__main__':

	#width = 1280
	#height = 720
	
	videoname = ''

	filename = 'some_paper.pdf'
	data = get_binary_string(filename)
	data, tail = display_data(data,(height,width))

	generate_video(f'{tail}.avi', data)
