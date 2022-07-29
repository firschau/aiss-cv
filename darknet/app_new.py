from flask import Flask, request, jsonify
from tensorflow import keras
import cv2
import numpy as np
import slot
import classes
from datetime import datetime


app = Flask(__name__)
app.config["DEBUG"] = True

# Load stored Keras model
model = keras.models.load_model('classifier.h5')
print("Loaded the keras model succesfully")
# Define image size
IMAGE_SIZE = 416

# Initialize Slots
slot_1 = slot.Slot()
slot_2 = slot.Slot()
slot_3 = slot.Slot()
slot_4 = slot.Slot()
slot_1.update_state(2)


detect_state = {"detect_list":""}


# ocr = PaddleOCR(use_angle_cls=True, lang='german')
# tool = language_tool_python.LanguageToolPublicAPI('de-DE') 

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
    #pascal_bb = yolo_to_pascal_voc(float(bb[1]),float(bb[2]),float(bb[3]),float(bb[4]),img.shape[0],img.shape[1])
    pascal_bb = bb
    x_min = int(pascal_bb[0])
    x_max = int(pascal_bb[1])
    y_min = int(pascal_bb[2])
    y_max = int(pascal_bb[3])
    cropped_img = img[y_min:y_max,
                      x_min:x_max]
    return(cropped_img)
    
def get_crop_ocr(image, yolo_bb):
    #pascal_bb = yolo_to_pascal_voc(yolo_bb[0],yolo_bb[1],yolo_bb[2],yolo_bb[3],image.shape[0],image.shape[1])
    img = cv2.imread(image)
    x_min = int(yolo_bb[0])
    x_max = int(yolo_bb[1])
    y_min = int(yolo_bb[2]-(yolo_bb[3]-yolo_bb[2])/10)
    y_max = int(yolo_bb[3]+(yolo_bb[3]-yolo_bb[2])*0.7)
    if y_max > image.shape[0]:
        y_max = int(image.shape[0])
    cropped_img = img[y_min:y_max,x_min:x_max]
    return cropped_img

def recognition(image):
    result = ocr.ocr(image, cls=True)
    words = []
    for box, word in result:
        words.append(word[0])
    sentence = ' '.join(words)
    return(tool.correct(sentence))

def detect_text(image, yolo_box):
    cropped = get_crop_ocr(image, yolo_box)
    text = recognition(cropped)
    return text


def slot_logic(prediction,text= ''):
    #TODO: What do we do with End Speed Restriction Class?

    if prediction == 12: 
        slot_1.update_state(2)
        slot_1.update_change()
    
    if prediction == 32: 
        slot_1.update_state(2)
        slot_1.update_change()
        return

    if prediction == 6:
        slot_1.update_state(2)
        slot_1.update_change()
        return        

    if prediction in classes.Slot1.__members__.values():
        slot_1.update_state(prediction)
        slot_1.update_change()
        return

    if prediction in classes.Slot2.__members__.values():
        slot_2.update_state(prediction)
        slot_2.update_change()
        return

    if prediction in classes.Slot3.__members__.values():
        slot_3.update_state(prediction)
        slot_3.update_change()
        return

    if prediction in classes.Slot4.__members__.values():
        slot_4.update_state(prediction)
        slot_4.update_change()
        return

    if isinstance(prediction, classes.EndRestrict):
        if prediction == classes.EndRestrict.END_OVERTAKING:
            if slot_2.state == classes.Overtaking.NO_OVERTAKING:
                slot_2.init_slot()
                return


def init_old_slots():
    #initialize slot 2 after 3 minutes (2.5km with speed 50km/h)
    if ((datetime.now() - slot_2.change).seconds) > 180:
        slot_2.__init__()

    #initialize slot 3 after 35s (500m with speed 50km/h)
    if ((datetime.now() - slot_3.change).seconds)> 35:
        slot_3.__init__()

    #initialize slot 4 after 20s (280m with speed 50km/h)
    if ((datetime.now() - slot_4.change).seconds)> 20:
        slot_4.__init__()



########################################################
#                                                      
#               POST Prediction Endpoint                                               
#                                                      
########################################################
@app.route('/<prediction>', methods=['POST'])
def predict(prediction):
    detect_state["detect_list"] = prediction
    
    return {"result": "success"}, 200

########################################################
#                                                      
#               GET Prediction Endpoint                                               
#                                                      
########################################################
@app.route("/inference", methods=["GET"])
def inference():
    detect_list = np.load("output.pkl",allow_pickle = True)
    print(detect_list)



    if detect_list.size > 1: 
        print("After if")
        #initialize slot sizes for checking for the biggest one
        slot_1_size = 0
        slot_2_size = 0
        slot_3_size = 0
        slot_4_size = 0
        person_flag = False

        # For each detected traffic signs in the prediction
        

            
        for pred, crop_img, x_center in  detect_list:
            print("in for schleife")
            print(pred,crop_img,x_center)
            if pred == 'person':
                #check if person bounding box is big enough
                if crop_img[0]*crop_img[1] < 0.02*IMAGE_SIZE**2:
                    continue

                #check if person bounding box is in center
                if x_center+(crop_img[0]/2)<0.1*IMAGE_SIZE or x_center-(crop_img[0]/2)>0.9*IMAGE_SIZE:
                    continue
                
                else:
                    person_flag = True
                    continue



            else:
                #skip if image is too far on the left
                #if x_center+(crop_img.shape[1]/2)<0.2*IMAGE_SIZE:
                    #continue
                
                # Get the current YOLOv4 image and crop out the detected bounding box area
                # cropped_img = read_and_crop_image(img, bb)
                
                #preprocess image in right input format
                cropped_img = cv2.cvtColor(crop_img, cv2.COLOR_RGB2BGR)
                cropped_img = cv2.resize(cropped_img,(30,30),3)
                cropped_img = np.expand_dims(cropped_img, axis=0)

                # Predict the traffic sign class for the cropped bounding box area with the Keras CNN
                predicted_class = model.predict(cropped_img)
                predictions = [float(i) for i in list(predicted_class[0])]
                print()
                
                
                if (max(predictions) > 0.7):
                    result_class = predictions.index(max(predictions))
                else:
                    continue

            
            # Check if biggest traffic sign 
            # Implement text in slot_logic if text is wanted
            if result_class in classes.Slot1.__members__.values() and slot_1_size < crop_img.size:
                slot_logic(result_class)
                slot_1_size = crop_img.size
            
            if result_class in classes.Slot2.__members__.values() and slot_2_size < crop_img.size:
                slot_logic(result_class)
                slot_2_size = crop_img.size

            if result_class in classes.Slot3.__members__.values() and slot_3_size < crop_img.size:
                slot_logic(result_class)
                slot_3_size = crop_img.size

            if result_class in classes.Slot4.__members__.values()  and slot_4_size < crop_img.size:
                slot_logic(result_class)
                slot_4_size = crop_img.size
                    
            
            init_old_slots()
            print(slot_1.get_slot(),slot_2.get_slot(),slot_3.get_slot(),slot_4.get_slot())
    
    return jsonify({'slot_1': slot_1.get_slot(), 
                'slot_2': slot_2.get_slot(), 
                'slot_3': slot_3.get_slot(), 
                'slot_4': slot_4.get_slot(), 
                'person': person_flag})
        


# Run the Flask app
app.run(debug=True)
