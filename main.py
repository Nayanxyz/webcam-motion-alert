import cv2
import av
import time
import threading
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from emailing import send_email  # This is your updated emailing.py


class MotionProcessor(VideoProcessorBase):
    def __init__(self):
        # 1. State Variables
        self.first_frame = None
        self.last_email_time = 0  # Initialize to 0 so the very first motion triggers an email
        self.cooldown = 60  # Wait 60 seconds between emails. Adjust as needed.

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        # OpenCV Math
        grey_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

        if self.first_frame is None:
            self.first_frame = grey_frame_gau
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        delta_frame = cv2.absdiff(self.first_frame, grey_frame_gau)
        thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
        contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 2. Motion Tracking Flag
        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue

            motion_detected = True  # We found an object large enough
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

            # 3. The Rate-Limiting Logic
            if motion_detected:
                current_time = time.time()

                if (current_time - self.last_email_time) > self.cooldown:
                    self.last_email_time = current_time

                    # IN-MEMORY UPGRADE:
                    # Do not touch the hard drive. Encode the image to memory.
                    success, buffer = cv2.imencode('.png', img)

                    if success:
                        # Convert the memory buffer to raw bytes
                        image_bytes = buffer.tobytes()

                        # Pass the bytes directly to the email thread
                        email_thread = threading.Thread(target=send_email, args=(image_bytes,))
                        email_thread.start()

        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Streamlit UI
st.title("Live Motion Security Alert")
st.write("Grant camera permissions to begin processing.")

webrtc_streamer(
    key="motion-detector",
    video_processor_factory=MotionProcessor,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)