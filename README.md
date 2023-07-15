# HEALTH STATUS DETECTION USING RASPBERRY PI AND AI

# Project Description

Innovative healthcare solutions are characterized as being non-invasive, affordable, having reduced response time, and easing the burden on caregivers for the elderly and individuals requiring continual care. This innovative project provides real-time monitoring and action state feedback on the state of medical patients. 

# General Overview
- From Dataset to Mediapipe to LSTM to Action State

# Model System Design
- The problem
- The LSTM model was chosen because it could take into account the sequential order of the predicted landmarks to be used for prediction
- Getting the Data
- Exploratory Data Analysis (Getting the video, No of Frames, No of Counts ...)
- Choosing Tensorflow vs Pytorch
- Training the model (Results)
- Describe how someone can use the code
- Post a snippet of it working
- Recommendations to improve the project or the model

# Hardware
- How the hardware works in general (Control System, align the camera frame with that of the image)

# Backend Description
- The system was created to stream the footage from the raspberry pi onto a client-facing web application.

### System Working Principle
- A persistent connection was created using sockets, to link the server with the raspberry pi.
- The pi transmits the data, which was encoded using OpenCV
- The footage was then converted to a moving jpeg format and streamed on the frontend.
  
### Tools Required
- Flask: To create the server
- Numpy and NumpySockets: To create a persistent link between the raspberry pi and our local server, through which the footage would be streamed
  
### Project Run Instructions
- To set up the project, run the following:
  ```
  pip install flask
  pip install opencv-python
  pip install numpy
  pip install numpysocket
  ```
- To launch the web application
  ```
  python3 main.py
  ```
  ![Home page](home.png)
  ![Working model](./web-screenshot.jpg)

### Project Recommendations
- Add servo control to the web application. Avoid lag
- Faster streaming. Increase FPS
