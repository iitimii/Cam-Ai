from client import client_rec

from flask import Flask, render_template, Response
import cv2
import os

app = Flask(__name__, static_folder='./static')

#camera = cv2.VideoCapture(0)

# Just added
# Global variables definition and initialization
global panServoAngle
global tiltServoAngle
panServoAngle = 90
tiltServoAngle = 90

panPin = 27
tiltPin = 17

# End of just added

@app.route('/')
def home():
      return render_template('home.html')

@app.route('/stream')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(client_rec(), mimetype='multipart/x-mixed-replace; boundary=frame')



# Pan Tilt control functions

@app.route('/camera')        
def camera():
    
    templateData = {
      'panServoAngle'	: panServoAngle,
      'tiltServoAngle'	: tiltServoAngle
	}
    
    return render_template('camera.html', **templateData)


if __name__ == '__main__':
    app.run(debug=True)