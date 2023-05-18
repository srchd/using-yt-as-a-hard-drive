import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys

from src.processing.utils import display_data
from src.processing.utils import get_binary_string

def main():

	import argparse

	parser = argparse.ArgumentParser(description="convert a file's binary to video frames, save video")
    parser.add_argument(
    	"--filename",
    	"-f",
    	help="the name of/path to the file to be converted"
    )
    parser.add_argument(
        "--width",
        "-w",
        type=int,
        help="width of the video (number of pixels)",
    )
    parser.add_argument(
        "--height",
        "-h",
        type=int,
        help="height of the video (number of pixels)",
    )


    args = parser.parse_args()

	data = get_binary_string(args.filename)
	data, tail = display_data(data,(args.height,args.width))

	frame_original = data[0,:,:,:]

	cap = cv2.VideoCapture('test_video.avi')

	ret, frame = cap.read()

	fig, axs = plt.subplots(1,2)
	axs[0].imshow(frame_original)
	axs[0].set_title('raw frame')
	axs[1].imshow(frame.astype(float))
	axs[1].set_title('retrieved from video')
	plt.show()

	cap.release()