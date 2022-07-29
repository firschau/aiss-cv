from darknet import *
import cv2
import numpy as np
import random 
import time


class Inference:

    def __init__(self):
        # Initialize Traffic Sign Yolo
        self.sign_cfg_path = '/home/nvidia/Projects/aiss-cv/darknet/cfg/yolov4-tiny_training.cfg'
        self.sign_classes_data_path = '/home/nvidia/Projects/aiss-cv/darknet/cfg/classes.data'
        self.sign_weights_path = '/home/nvidia/Projects/aiss-cv/darknet/yolov4-tiny_training_last.weights'
        self.sign_thresh = 0.5
        self.sign_network, self.sign_class_names, self.sign_class_colors = load_network(self.sign_cfg_path, self.sign_classes_data_path, self.sign_weights_path)
        self.sign_darknet_width =network_width(self.sign_network)
        self.sign_darknet_height =network_height(self.sign_network)

        # Initialize Person Yolo
        self.pers_cfg_path = '/home/nvidia/Projects/darknet/cfg/custom-yolov4-tiny.cfg'
        self.pers_coco_data_path = '/home/nvidia/Projects/darknet/cfg/coco.data'
        self.pers_weights_path = '/home/nvidia/Projects/darknet/yolov4-tiny.weights'
        self.pers_network, self.pers_class_names, self.pers_class_colors = load_network(self.pers_cfg_path, self.pers_coco_data_path, self.pers_weights_path)
        self.pers_darknet_width =network_width(self.pers_network)
        self.pers_darknet_height =network_height(self.pers_network)
        self.pers_thresh = 0.4


        self.cap = cv2.VideoCapture(self.gstreamer_pipeline(
                    capture_width=416, capture_height=416,
                    flip_method=0),cv2.CAP_GSTREAMER)


    def gstreamer_pipeline(self,
        sensor_id=0,
        capture_width=416,
        capture_height=416,
        display_width=416,
        display_height=416,
        framerate=30,
        flip_method=0,
    ):
        return (
            "nvarguscamerasrc sensor-id=%d !"
            "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
            "nvvidconv flip-method=%d ! "
            "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
            "videoconvert ! "
            "video/x-raw, format=(string)BGR ! appsink"
            % (
                sensor_id,
                capture_width,
                capture_height,
                framerate,
                flip_method,
                display_width,
                display_height,
            )
        )


    def crop(self,img,detections):
        for i in range(len(detections)):

            x_min = int(detections[i][2][2])
            x_max = int(detections[i][2][3])
            y_min = int(detections[i][2][0])
            y_max = int(detections[i][2][1])
            print(x_min,x_max,y_min,y_max)
            crop_img = img[x_min:x_max,y_min:y_max]
            cv2.imshow("cropped_img", crop_img)
            cv2.waitKey(0)


    def conv_crop1(self,img, detections):
        img_height, img_width, _ = img.shape
        for i in range(len(detections)):
            x_min = int(detections[i][2][0])
            x_max = int(x_min + detections[i][2][2])
            y_max = int(detections[i][2][1])
            y_min = int(y_max -detections[i][2][3])
            crop_img = img[x_min:x_max,y_min:y_max]
            cv2.imshow("cropped img", crop_img)
            cv2.waitKey(0)


    def conv_crop(self, img, bbox):
        """Crops a image depending on bounding box 

        Parameter
        ---------
        img: array
            The image that needs to be cropped
        bbox: list
            The Bounding Box that should be cropped out of image
            with format: [x_center, y_center, bbox_widht, bbox_heigth]

        Returns
        -------
        image:array
            The cropped image
            
        """

        x, y, w, h = bbox
        
        image_h, image_w, __ = img.shape

        left = int(x - w / 2.)
        right = int(x + w / 2.)
        top = int(y + h / 2.)
        bottom = int(y - h / 2.)

        if (left < 0):
            left = 0
        if (right > image_w - 1):
            right = image_w - 1
        if (top > image_h-1):
            top = image_h-1
        if (bottom < 0):
            bottom = 0

        crop_img = img[bottom:top,left:right]
        
        return crop_img
    

     
    def convert2relative(self, bbox):
        """
        YOLO format use relative coordinates for annotation
        """
        x, y, w, h = bbox
        _height = self.sign_darknet_height
        _width = self.sign_darknet_width
        return x/_width, y/_height, w/_width, h/_height


    def convert2original(self, image, bbox):
        x, y, w, h = self.convert2relative(bbox)

        image_h, image_w, __ = image.shape

        orig_x = int(x * image_w)
        orig_y = int(y * image_h)
        orig_width = int(w * image_w)
        orig_height = int(h * image_h)

        bbox_converted = (orig_x, orig_y, orig_width, orig_height)

        return bbox_converted


    def convert4cropping(self, image, bbox):
        x, y, w, h = self.convert2relative(bbox)

        image_h, image_w, __ = image.shape

        orig_left = int((x - w / 2.) * image_w)
        orig_right = int((x + w / 2.) * image_w)
        orig_top = int((y - h / 2.) * image_h)
        orig_bottom = int((y + h / 2.) * image_h)

        if (orig_left < 0):
            orig_left = 0
        if (orig_right > image_w - 1):
            orig_right = image_w - 1
        if (orig_top < 0):
            orig_top = 0
        if (orig_bottom > image_h - 1):
            orig_bottom = image_h - 1

        bbox_cropping = (orig_left, orig_top, orig_right, orig_bottom)
        
        return bbox_cropping
    

    def video_capture(self, frame):

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.sign_darknet_width, self.sign_darknet_height),
                                    interpolation=cv2.INTER_LINEAR)
        
        img_for_detect = make_image(
            self.sign_darknet_width, self.sign_darknet_height, 3)
        copy_image_from_bytes(
            img_for_detect, frame_resized.tobytes())
        return img_for_detect

                
    def inference(self):
        """Does one inference loop 

        Returns
        -------
        list
            a nested list: [[class,cropped_img,x_center],...]
        """

        # Make sure to get a frame
        while True:
            ret, frame = self.cap.read()
            if frame is not None:
                break
            if frame is None:
                print("Didnt catch a frame")

        prev_time = time.time()
        darknet_image = self.video_capture(frame)
        detections = detect_image(
        self.sign_network, self.sign_class_names, darknet_image, thresh=self.sign_thresh)

        #print_detections(detections)
        
        

        detect_list = []
        for label, confidence, bbox in detections:
            
            bbox_adjusted = self.convert2original(frame, bbox)
            detect_list.append([str(label),self.conv_crop(frame, bbox_adjusted),bbox[0]/frame.shape[1]]) 

        #Send frame through Person Yolo
        detections = detect_image(
        self.pers_network, self.pers_class_names, darknet_image, thresh=self.pers_thresh)

        for label, confidence, bbox in detections:
            if str(label) == "person":
                bbox_adjusted = self.convert2original(frame, bbox)
                detect_list.append([str(label),[bbox[2],bbox[3]],bbox[0]/frame.shape[1]])
                print(label) 

        fps = int(1/(time.time() - prev_time))
        print("With 2xYolo + Cropping FPS: {}".format(fps))
        free_image(darknet_image)
        detect_list = np.asarray(detect_list,dtype=object)
        if detect_list.size >1:
            detect_list.dump("output.pkl")




        
 

        return detect_list
	
