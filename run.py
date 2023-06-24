import numpy as np
import cv2
from collections import deque
import mediapipe as mp
import tensorflow.lite as lite
from picamera2 import Picamera2
from pantilthat import pan, tilt
#import time

SEQ_LEN = 10

CLASSES_LIST =  ['Fall Down',
 'Sitting down',
 'Walking',
 'Lying down',
 'Standing up',
 'Standing',
 'Sitting',
 'Chest Pain',
 'Coughing',']

TF_LITE_MODEL_NAME = 'final_model.tflite

interpreter = lite.Interpreter(TF_LITE_MODEL_NAME)

x = 0
y = 0
dx = 3
dy = 1.5
prev_time = 0

pan(0)
tilt(0)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.65, min_tracking_confidence=0.5, model_complexity=1)
mp_draw = mp.solutions.drawing_utils


pan(x)
tilt(y)
 



def tflite_predict(X, interpreter):
    interpreter.allocate_tensors()
    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], np.expand_dims(X, 0))
    interpreter.invoke()
    predictions = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
    return predictions


def pred_video(interpreter, SEQUENCE_LENGTH=SEQ_LEN):
    
    piCam=Picamera2()
    piCam.preview_configuration.main.size = (720, 480)
    piCam.preview_configuration.main.format = "RGB888"
    piCam.preview_configuration.align()
    piCam.configure("preview")
    piCam.start()
    
    x = 0
    y = 22
    
    pan(x)
    tilt(y)
    cx =0
    cy = 0
    reset = 0
    
    frames_queue = deque(maxlen = SEQUENCE_LENGTH)
    predicted_class_name = ''
    while True:
        frame = piCam.capture_array()
        frame = cv2.flip(frame, 0)
        
        h,w,c = frame.shape

        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        if results.pose_landmarks:
        
            lm = results.pose_landmarks.landmark[0]
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(frame, (cx,cy), 7, (255, 0, 0), cv2.FILLED)
        
            if cx>430 and x<85:
                x+=dx
    
            if cx<290 and x>-85:
                x-=dx
        
            if cy<100 and y>-85:
                y-=dy
    
            if cy>180 and y<85:
                y+=dy
        else:
            reset+=1
            if reset > 40:
                x=0
                y=30
            
        pan(x)
        tilt(y) 
        

        pose_lm = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten()  if results.pose_landmarks else np.zeros(132)
        
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) 

        frames_queue.append(pose_lm.astype('float32'))

        if len(frames_queue) == SEQUENCE_LENGTH:
            
            predicted_labels_probabilities = tflite_predict(frames_queue, interpreter)
            
            predicted_label = np.argmax(predicted_labels_probabilities)

            predicted_class_name = CLASSES_LIST[predicted_label]


        cv2.putText(frame, predicted_class_name, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5) if results.pose_landmarks else cv2.putText(frame, 'No Action', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1)== ord('q'):
            cv2.destroyAllWindows()
            break

    


pred_video(interpreter)
