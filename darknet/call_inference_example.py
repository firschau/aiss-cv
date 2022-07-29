from inference import Inference
import cv2
import time


# This is just for test and show purposes

inf = Inference()

while True:
	
	
	detect_list = inf.inference()

	
	for pred, crop_img, x_center in detect_list:
		print(x_center)
		print(pred)



