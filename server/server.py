from flask import Flask
from flask_ngrok import run_with_ngrok
from tensorflow import keras
import cv2
import os
import time

app = Flask(__name__)
run_with_ngrok(app)

# Convert YOLO coordinates to Pascal VOC
def yolo_to_pascal_voc(x_center, y_center, w, h,  image_w, image_h):
    w = w * image_w
    h = h * image_h
    x1 = ((2 * x_center * image_w) - w)/2
    y1 = ((2 * y_center * image_h) - h)/2
    x2 = x1 + w
    y2 = y1 + h
    return [x1, y1, x2, y2]

# Crop out image part based on bounding boxes
def read_and_crop_image(img, bb):
    img = cv2.imread(img)
    pascal_bb = yolo_to_pascal_voc(bb[0],bb[1],bb[2],bb[3],img.shape[0],img.shape[1])
    x_min = int(pascal_bb[0])
    x_max = int(pascal_bb[2])
    y_min = int(pascal_bb[1])
    y_max = int(pascal_bb[3])
    cropped_img = img[y_min:y_max,x_min:x_max]
    return(cropped_img)

# Load stored Keras model
model = keras.models.load_model('model.h5')

########################################################
#                                                      
#               Main Prediction Endpoint                                               
#                                                      
########################################################
@app.route("/")
def predict():

  result = {
    "slot_1": "",
    "slot_2": "",
    "slot_3": "",
    "slot_4": ""
  }

  # Get the current YOLOv4 prediction
  with open('yolo.txt', 'r') as prediction:
    # For each detected traffic signs in the prediction
    for detection in prediction:
        # Get the current YOLOv4 image and crop out the detected bounding box area
        cropped_img = read_and_crop_image("path", detection)

        # Predict the traffic sign class for the cropped bounding box area with the Keras CNN
        predicted_class = model.predict(cropped_img)

        # TO-DO: logic

  return result

# Run the Flask app
app.run()