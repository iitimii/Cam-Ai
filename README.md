# HEALTH STATUS DETECTION USING RASPBERRY PI AND AI

# Project Description

Innovative healthcare solutions are characterized as being non-invasive, affordable, having reduced response time, and easing the burden on caregivers for the elderly and individuals requiring continual care. This innovative project provides real-time monitoring and action state feedback on the state of medical patients. 

https://github.com/iitimii/Raspberry-Pi-Tracking-Camera-plus-Action-Recognition/assets/106264110/a167cb20-c324-4fc2-b70b-95f00f128698

# Hardware
The hardware is a [Pimoroni pan-tilt hat camera](https://shop.pimoroni.com/products/pan-tilt-hat?variant=22408353287) with an onboard microcontroller which lets you independently drive the two servos (pan and tilt). The module pans and tilts through 180 degrees on each axis and is compatible with all 40-pin header Raspberry Pi models.

<img width="454" alt="Screenshot 2023-07-23 at 01 22 09" src="https://github.com/iitimii/Raspberry-Pi-Tracking-Camera-plus-Action-Recognition/assets/44223263/7430d87b-722b-434a-8158-15253fff86fa">

# System Design
- The pan-tilt camera centers on a subject by controlling the servos to minimize the error between the nose of the subject and the center of the camera's view using a bang-bang controller.
- From Dataset to Mediapipe to LSTM to Action State
- The system is designed to monitor the actions of a patient
- Mediapipe was used to extract the landmarks from the video frames 
- The LSTM model was chosen because it could take into account the sequential order of the extracted landmarks to be used for prediction
- The LSTM model uses a sequence of ten successive frames to determine the patient's action
- TensorFlow is faster for creating small models for small projects like this that’s why it was chosen as the deep learning engine

# Model Results
- The model achieved the following results
- Loss: 0.5894
- Accuracy: 0.7817
- Val_Loss: 0.8967
- Val_Accuracy: 0.6873

![image](https://github.com/iitimii/Raspberry-Pi-Tracking-Camera-plus-Action-Recognition/assets/106264110/b2c35307-8bd2-4397-8cec-865dc3f9431d)

![image](https://github.com/iitimii/Raspberry-Pi-Tracking-Camera-plus-Action-Recognition/assets/106264110/eb922d3a-422a-43fd-96d0-6b33a544aaee)

![image](https://github.com/iitimii/Raspberry-Pi-Tracking-Camera-plus-Action-Recognition/assets/106264110/b7ccef6f-055a-4deb-8443-e659c45c9908)

# Backend Description
The backend handles the streaming of the footage from the Raspberry Pi onto a client-facing web application.

### Backend Working Principle
- A persistent connection was created using sockets, to link the server with the Raspberry Pi.
- The pi transmits the data, which is encoded using OpenCV
- The footage was then converted to a moving jpeg format and streamed on the front end.
  
### Tools Required for the Backend
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

### Project Run Instructions
- To run the program without the web app:
- Transfer the ```run.py``` file to the raspberry pi using the ```scp``` comand (secure copy)
- ```scp <source-file> <user>@<host_ip_address>:<path> ```
- run the ```run.py``` file on the raspberry pi

# Recommendations
- Add servo control to the web application.
- Faster streaming. Increase FPS to avoid lag.
- Training with more data as the model struggles with standing and walking

https://github.com/iitimii/Raspberry-Pi-Tracking-Camera-plus-Action-Recognition/assets/106264110/a0121018-6a20-448e-89c3-6228e23cdeaa

