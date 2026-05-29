# 📹 Motion Detection and Email Alert System
A lightweight, Python-based computer vision application that monitors a live webcam feed for motion. When an object enters the frame, the system tracks it, captures a series of images, and automatically sends an email alert with a captured snapshot once the object leaves the camera's view.

### 📸 Project Screenshots
<img width="1687" height="673" alt="Screenshot 2026-05-29 131127" src="https://github.com/user-attachments/assets/f1633113-d6d6-4bdd-b857-f21ad44c9061" />


 ## Caption: Live video feed showing the green bounding box tracking a moving object.

 
 <img width="1698" height="697" alt="Screenshot 2026-05-29 131147" src="https://github.com/user-attachments/assets/535901ee-6f6c-490c-a144-bfa807689787" />



 ## Caption: Automated email alert delivered to the inbox with the captured snapshot attached.

 
  <img width="1894" height="809" alt="Screenshot 2026-05-29 131534" src="https://github.com/user-attachments/assets/9116c76e-4452-4747-83ab-15aef93fff10" />


## *✨ Key Features*
## 🎯 Real-Time Motion Detection:
Utilizes OpenCV for frame differencing, Gaussian blurring, and contour detection to accurately identify moving objects.

## 📧 Automated Email Alerts:
Sends an email with an attached image of the detected object using background threading, ensuring the video feed remains uninterrupted.

## 🟩 Dynamic Tracking:
Draws precise green bounding boxes around moving objects in the live video feed.

## 🧹 Automated Cleanup:
Automatically clears locally saved image frames after the background process is complete to save disk space.

## ⚙️ Prerequisites
Ensure you have Python 3.x installed on your system. The script relies on the following standard and external libraries:

opencv-python

time (Standard Library)

glob (Standard Library)

os (Standard Library)

threading (Standard Library)

⚠️ Note: The script imports a custom function send_email from a local emailing.py file. You will need to configure this file with your specific SMTP server and email credentials for the alerts to work.

### 🚀 Installation
1. Clone the repository

```Bash
git clone https://github.com/Nayanxyz/webcam-motion-alert.git

cd webcam-motion-alert
```
2. Install dependencies

```Bash
pip install opencv-python
```
3. Configure the Email Module
Ensure you have an emailing.py file in the root directory with a send_email(image_path) function configured to handle your specific email provider's SMTP protocol.

## 💻 Usage
Execute the main Python script to start the webcam feed and motion detection:

```Bash
python main.py
```
## 🎮 Controls:

Press the q key while the video window is active to safely terminate the application and trigger the final folder cleanup.

## 🧠 How It Works
Baseline Generation: The script captures the first frame, converts it to grayscale, and applies a Gaussian blur to serve as the static background baseline.

Delta Calculation: Subsequent frames are compared against the baseline using absolute difference (cv2.absdiff).

Thresholding & Dilation: The difference is converted into a binary image and dilated to fill in gaps, making object detection cleaner.

Contour Mapping: The script finds the contours of the dilated image. If a contour exceeds 5000 pixels, it is flagged as a valid moving object.

Image Capture & Emailing: Images are saved locally while the object is in the frame. When the object exits, a background thread selects the median image from the sequence and emails it.

## 📜 License
Distributed under the MIT License. See LICENSE for more information.
