from inference import Inference
import cv2

# This is just for test and show purposes

inf = Inference()
i=0
while True:
	i+=1
	classes, cropped_imgs, x_centers = inf.inference()
	if i%20 ==0:
		for crop_img in cropped_imgs:

			cv2.imshow("cropped img", crop_img)
			cv2.waitKey(0)

