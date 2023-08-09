
import os
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import tensorflow as tf
import argparse
import sys
import RPi.GPIO as GPIO
import time

from twilio.rest import Client

account_sid = os.environ['xxxxxxxxxxxxxxxxxxxxxxxx']
auth_token = os.environ['xxxxxxxxxxxxxxxxxxxxxxxxxxx']
my_number = os.environ['+1xxxxxxxxxxxxxxx']
twilio_number = os.environ['+1xxxxxxxxxxxxxxxx']

client = Client(account_sid,auth_token)

IM_WIDTH = 1280
IM_HEIGHT = 720

camera_type = 'picamera'
parser = argparse.ArgumentParser()
parser.add_argument('--usbcam', help='Use a USB webcam instead of picamera',
                    action='store_true')
args = parser.parse_args()
if args.usbcam:
    camera_type = 'usb'

sys.path.append('..')

from utils import label_map_util
from utils import visualization_utils as vis_util

MODEL_NAME = 'ssdlite_mobilenet_v2_coco_2018_05_09'

CWD_PATH = os.getcwd()

PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

PATH_TO_LABELS = os.path.join(CWD_PATH,'data','mscoco_label_map.pbtxt')

NUM_CLASSES = 90

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

    sess = tf.Session(graph=detection_graph)

image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')

detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

num_detections = detection_graph.get_tensor_by_name('num_detections:0')


frame_rate_calc = 1
freq = cv2.getTickFrequency()
font = cv2.FONT_HERSHEY_SIMPLEX


detected_harmful = False
detected_nonharmful = False

harmful_counter = 0
nonharmful_counter = 0

pause = 0
pause_counter = 0

#### detection function ####

def ani_detector(frame):

    global detected_harmful, detected_nonharmful
    global harmful_counter, nonharmful_counter
    global pause, pause_counter

    frame_expanded = np.expand_dims(frame, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores, detection_classes, num_detections],
        feed_dict={image_tensor: frame_expanded})

    vis_util.visualize_boxes_and_labels_on_image_array(
        frame,
        np.squeeze(boxes),
        np.squeeze(classes).astype(np.int32),
        np.squeeze(scores),
        category_index,
        use_normalized_coordinates=True,
        line_thickness=8,
        min_score_thresh=0.40)
    
    if (((int(classes[0]) == 23) or (int(classes[0] == 24) or (int(classes[0]) == 25) or (int(classes[0] == 26))) and (pause == 0)):
        x = int(((boxes[0][0][1]+boxes[0][0][3])/2)*IM_WIDTH)
        y = int(((boxes[0][0][0]+boxes[0][0][2])/2)*IM_HEIGHT)

            harmful_counter = harmful_counter + 1
        
    if (((int(classes[0]) == 17) or (int(classes[0] == 18) or (int(classes[0]) == 19) or (int(classes[0] == 20) or (int(classes[0] == 21) or (int(classes[0] == 22))) and (pause == 0)):
        x = int(((boxes[0][0][1]+boxes[0][0][3])/2)*IM_WIDTH)
        y = int(((boxes[0][0][0]+boxes[0][0][2])/2)*IM_HEIGHT)

        nonharmful_counter = nonharmful_counter + 1    

    if harmful_counter > 10:
        detected_harmful = True
        message = client.messages.create(
            body = 'Harmful Animal Detected',
            from_=twilio_number,
            to=my_number
            )
        harmful_counter = 0
        nonharmful_counter = 0
        pause = 1

    if nonharmful_counter > 10:
        detected_nonharmful = True
        message = client.messages.create(
            body = 'Non harmful animal Detected',
            from_=twilio_number,
            to=my_number
            )
        harmful_counter = 0
        nonharmful_counter = 0
        pause = 1

    if pause == 1:
        if detected_Harmful == True:
            cv2.putText(frame,'Harmful Animal Detected',(int(IM_WIDTH*.1),int(IM_HEIGHT*.5)),font,3,(0,0,0),7,cv2.LINE_AA)
            cv2.putText(frame,'Harmful Animal Detected',(int(IM_WIDTH*.1),int(IM_HEIGHT*.5)),font,3,(95,176,23),5,cv2.LINE_AA)

        if detected_nonharmful == True:
            cv2.putText(frame,'Non harmful animal Detected',(int(IM_WIDTH*.1),int(IM_HEIGHT*.5)),font,3,(0,0,0),7,cv2.LINE_AA)
            cv2.putText(frame,'Non harmful animal Detected',(int(IM_WIDTH*.1),int(IM_HEIGHT*.5)),font,3,(95,176,23),5,cv2.LINE_AA)

        pause_counter = pause_counter + 1
        if pause_counter > 30:
            pause = 0
            pause_counter = 0
            detected_harmful = False
            detected_nonharmful = False

    cv2.putText(frame,'Detection counter: ' + str(max(harmful_counter,nonharmful_counter)),(10,100),font,0.5,(255,255,0),1,cv2.LINE_AA)
    cv2.putText(frame,'Pause counter: ' + str(pause_counter),(10,150),font,0.5,(255,255,0),1,cv2.LINE_AA)

    return frame


### Picamera ###
if camera_type == 'picamera':
    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

    for frame1 in camera.capture_continuous(rawCapture, format="bgr",use_video_port=True):

        t1 = cv2.getTickCount()
        
        frame = frame1.array
        frame.setflags(write=1)

        frame = ani_detector(frame)

        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

        cv2.imshow('Object detector', frame)

        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        if cv2.waitKey(1) == ord('q'):
            break

        rawCapture.truncate(0)

    camera.close()

### USB webcam ###
    
elif camera_type == 'usb':
    camera = cv2.VideoCapture(0)
    ret = camera.set(3,IM_WIDTH)
    ret = camera.set(4,IM_HEIGHT)

    while(True):

        t1 = cv2.getTickCount()

        ret, frame = camera.read()

        frame = ani_detector(frame)

        cv2.putText(frame,"FPS: {0:.2f}".format(frame_rate_calc),(30,50),font,1,(255,255,0),2,cv2.LINE_AA)

        cv2.imshow('Object detector', frame)

        t2 = cv2.getTickCount()
        time1 = (t2-t1)/freq
        frame_rate_calc = 1/time1

        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
        
cv2.destroyAllWindows()
