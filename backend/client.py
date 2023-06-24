import logging
import numpy as np
from numpysocket import NumpySocket
import cv2

#logger = logging.getLogger('OpenCV server')
#logger.setLevel(logging.INFO)

def client_rec():
    with NumpySocket() as s:
        s.bind(('', 9999))
        frame_count = 0
        while True:
            try:
                s.listen()
                conn, addr = s.accept()
                conn.sendall(np.array([0,0]))            
                #logger.info(f"connected: {addr}")
                while conn:
                    frame = conn.recv()
                    if len(frame) == 0:
                        break
                    frame_count += 1
                    #c v2.imshow('Frame', frame)
                    print(frame_count)

                    #newframe = cv2.resize(frame,(int(0.5),int(0.5)))
                    ret, buffer = cv2.imencode('.jpg', frame)
                    # newframe = cv2.resize(frame, (10, 10))
                    # newframe = buffer.tobytes()
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                    
                    
                #logger.info(f"disconnected: {addr}")
            except ConnectionResetError:
                pass
