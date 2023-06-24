import numpy as np
import cv2
from collections import deque
import mediapipe as mp
import tensorflow.lite as lite
from picamera2 import Picamera2
from pantilthat import pan, tilt

SEQ_LEN = 10

CLASSES_LIST =  ['Fall Down',
 'Sitting down',
 'Walking',
 'Lying down',
 'Standing up',
 'Standing',
 'Sitting',
 'Chest Pain',
 'Coughing']

TF_LITE_MODEL_NAME = 'final_model.tflite'

interpreter = lite.Interpreter(TF_LITE_MODEL_NAME)

x = 0
y = 0
dx = 2
dy = 2

center_x = 360
center_y = 120
threshold_x = 100
threshold_y = 40

pan(0)
tilt(0)


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.7, min_tracking_confidence=0.5, model_complexity=1)
mp_draw = mp.solutions.drawing_utils


pan(x)
tilt(y)

 



def tflite_predict(X, interpreter):
    interpreter.allocate_tensors()
    interpreter.set_tensor(interpreter.get_input_details()[0]['index'], np.expand_dims(X, 0))
    interpreter.invoke()
    predictions = interpreter.get_tensor(interpreter.get_output_details()[0]['index'])
    return predictions
    

    
    
def track_control(results, frame, x, y, w, h, reset):
    if results.pose_landmarks:
        reset = 0
        
        lm = results.pose_landmarks.landmark[0]
        cx, cy = int(lm.x*w), int(lm.y*h)
        cv2.circle(frame, (cx,cy), 7, (255, 0, 0), cv2.FILLED)
        
        if cx>(center_x + threshold_x) and x<85:
            x+=dx
    
        if cx<(center_x - threshold_x) and x>-85:
            x-=dx
        
        if cy<(center_y - threshold_y) and y>-85:
            y-=dy
     
        if cy>(center_y + threshold_y) and y<85:
            y+=dy
    else:
        reset+=1
    return frame, x, y, reset

    
    


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
    mode = 'track'
    
    frames_queue = deque(maxlen = SEQUENCE_LENGTH)
    global predicted_class_name = ''
    while True:
        key_pressed = cv2.waitKey(1)
        frame = piCam.capture_array()
        frame = cv2.flip(frame, 0)
        
        h,w,c = frame.shape

        #frame = cv2.resize(frame, (256, 256))

        results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        ######## keyboard or track control
        if mode == 'track':
            frame, x, y, reset = track_control(results, frame, x, y, w, h, reset)
            cv2.putText(frame, "press 'k' for keyboard control", (220, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            
        if mode == 'keyboard':
            reset = 0
            if key_pressed== ord('a') and x>-85:
                x-=dx
    
            elif key_pressed== ord('d') and x<85:
                x+=dx
        
            elif key_pressed== ord('s') and y<85:
                y+=dy
     
            elif key_pressed== ord('w') and y>-85:
                y-=dy
                
            cv2.putText(frame, "w-up", (580, 270), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "s-down", (580, 310), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "a-left", (580, 350), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, "d-right", (580, 390), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
            cv2.putText(frame, "press 't' for AI tracking", (320, 470), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            
        if reset == 40:
            x=0
            y=18
            
        if reset > 45:
            if x<85:
                x+=(dx*0.5)
            if x>=85:
                x=-85
            if y<30:
                y+=(dy*0.2)
            if y>=30:
                y=10
            
            
        pan(x)
        tilt(y) 
        

        pose_lm = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten()  if results.pose_landmarks else np.zeros(132)
        
        mp_draw.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS) 

        frames_queue.append(pose_lm.astype('float32'))

        if len(frames_queue) == SEQUENCE_LENGTH:
            
            predicted_labels_probabilities = tflite_predict(frames_queue, interpreter)
            
            predicted_label = np.argmax(predicted_labels_probabilities)

            predicted_class_name = CLASSES_LIST[predicted_label]


        cv2.putText(frame, predicted_class_name, (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4) if results.pose_landmarks else cv2.putText(frame, 'No Action', (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5)
        cv2.putText(frame, "press 'q' to exit", (420, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.imshow('frame', frame)
        
        
        if key_pressed== ord('q'):
            cv2.destroyAllWindows()
            break
        
        if key_pressed== ord('k'):
            mode = 'keyboard'
            
        if key_pressed== ord('t'):
            mode = 'track'
            
        

        
    


pred_video(interpreter)
