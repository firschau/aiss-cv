from darknet import *
import cv2
import jetson.utils

class Inference:

    def __init__(self,width = 1280, height=720):
        self.cfg_path = '/home/nvidia/Projects/darknet/cfg/custom-yolov4-tiny.cfg'
        self.coco_data_path = '/home/nvidia/Projects/darknet/cfg/coco.data'
        self.weights_path = '/home/nvidia/Projects/darknet/yolov4-tiny.weights'
        self.detections = None
        self.cap = cv2.VideoCapture(self.gstreamer_pipeline(
                            capture_width=416, capture_height=416,
                            flip_method=0),cv2.CAP_GSTREAMER)
        self.network, self.class_names, self.class_colors = load_network(self.cfg_path, self.coco_data_path, self.weights_path)
        self.width = network_width(self.network)
        self.height = network_height(self.network)



    # darknet helper function to run detection on image
    def darknet_helper(self, img, width, height):
        darknet_image = make_image(width, height, 3)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_resized = cv2.resize(img_rgb, (width, height),
                                    interpolation=cv2.INTER_LINEAR)

        # get image ratios to convert bounding boxes to proper size
        img_height, img_width, _ = img.shape
        width_ratio = img_width/width
        height_ratio = img_height/height

        # run model on darknet style image to get detections
        copy_image_from_bytes(darknet_image, img_resized.tobytes())
        detections = detect_image(self.network, self.class_names, darknet_image)
        free_image(darknet_image)
        return detections, width_ratio, height_ratio


    def gstreamer_pipeline(self,
        sensor_id=0,
        capture_width=1920,
        capture_height=1080,
        display_width=960,
        display_height=540,
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



    def inference(self):

        ret, frame = self.cap.read()
        #if cv2.waitKey(1) & 0xFF == ord('q'):
        #    break
        detections, width_ratio, height_ratio = self.darknet_helper(frame, self.width, self.height)
        return detections



	
        """
        for label, confidence, bbox in detections:
        left, top, right, bottom = bbox2points(bbox)
        left, top, right, bottom = int(left * width_ratio), int(top * height_ratio), int(right * width_ratio), int(bottom * height_ratio)
        cv2.rectangle(image, (left, top), (right, bottom), class_colors[label], 2)
        cv2.putText(image, "{} [{:.2f}]".format(label, float(confidence)),
                        (left, top - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        class_colors[label], 2)
        """

	
	
