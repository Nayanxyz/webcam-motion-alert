# 📹 Smart Security: Motion Detection & Automated Alert System
A lightweight, automated computer vision application built in Python. This system monitors a live webcam feed for unauthorized motion, dynamically tracks moving objects, captures physical evidence, and dispatches automated email alerts with image attachments in real time.

Designed for low-overhead security monitoring, it leverages OpenCV for frame analysis and Python's native threading to ensure the video feed remains uninterrupted while network tasks execute in the background.

### 📸 Project Screenshots
<img width="1687" height="673" alt="Screenshot 2026-05-29 131127" src="https://github.com/user-attachments/assets/f1633113-d6d6-4bdd-b857-f21ad44c9061" />


 ## Caption: Live video feed showing the green bounding box tracking a moving object.

 
 <img width="1698" height="697" alt="Screenshot 2026-05-29 131147" src="https://github.com/user-attachments/assets/535901ee-6f6c-490c-a144-bfa807689787" />



 ## Caption: Automated email alert delivered to the inbox with the captured snapshot attached.

 
  <img width="1894" height="809" alt="Screenshot 2026-05-29 131534" src="https://github.com/user-attachments/assets/9116c76e-4452-4747-83ab-15aef93fff10" />

## 🚀 Key Features
Real-Time Frame Differencing: Utilizes OpenCV background subtraction, Gaussian blurring, and thresholding to filter out noise and isolate genuine physical movement.

Intelligent Object Tracking: Maps extreme outer contours and draws dynamic bounding boxes around moving targets in the live feed.

Asynchronous Alerting: Employs Python threading to dispatch SMTP email alerts with image attachments without blocking or lagging the primary video capture loop.

Automated Evidence Management: Captures a sequence of frames while the subject is in view, emails the optimal median frame, and automatically cleans up local storage once the alert is sent.

## 🛠️ System Architecture
The project is divided into two primary modules:

main.py: The core computer vision engine. Handles the video stream, mathematical frame comparison, contour mapping, image saving, and thread management.

email.py: The notification engine. Establishes a secure TLS-encrypted connection with Gmail's SMTP servers to format and dispatch the alert payload.

## ⚙️ Prerequisites & Setup
Ensure you have Python 3.9+ installed.

1. Clone the repository

```Bash
git clone https://github.com/Nayanxyz/webcam-motion-alert.git
cd webcam-motion-alert
```
2. Install dependencies

```Bash
pip install opencv-python python-dotenv
```
(Note: os, time, glob, threading, smtplib, and email are part of the Python Standard Library).

3. Configure Environment Variables (Security)
Never hardcode your email credentials. Create a .env file in the root directory of the project:

Code snippet
```
SENDER_EMAIL="your_email@gmail.com"
RECEIVER_EMAIL="target_email@gmail.com"
EMAIL_PASSWORD="your_google_app_password"
```
Note: If using Gmail, you must generate an App Password via your Google Account Security settings; standard account passwords will not work for SMTP connections.

## 💻 Usage
Execute the main engine to initialize the camera feed and begin monitoring:

```Bash
python main.py
```
## Operational Controls:

The system will open a window displaying the live feed with tracking enabled.

Press the q key while the video window is active to safely terminate the process and trigger the final storage cleanup thread.

## 🧠 Algorithmic Flow
Baseline Initialization: The system captures the initial frame, converts it to grayscale, and applies a 21x21 Gaussian blur to establish a static environmental baseline.

Delta Calculation: Subsequent frames are continuously compared against the baseline using cv2.absdiff().

Binary Thresholding & Dilation: The absolute difference is converted into a binary matrix (black/white) and dilated to fill structural holes, solidifying the object's mass.

Contour Extraction: cv2.findContours() maps the boundaries. Noise is filtered out by ignoring contours with an area of less than 5000 pixels.

State Machine & Threading: * State 0 (Idle): No motion.

State 1 (Active): Object detected. Images are continuously saved to /images.

State Transition (1 -> 0): Object exits the frame. A daemon thread is spawned to email the median image, while a secondary thread flushes the local /images directory.

## 📜 License
Distributed under the MIT License. See LICENSE for more information.

