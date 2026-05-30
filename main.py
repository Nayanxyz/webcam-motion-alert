import cv2
import av
import time
import threading
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from emailing import send_email


class MotionProcessor(VideoProcessorBase):
    def __init__(self):
        self.first_frame = None
        self.last_email_time = 0
        self.cooldown = 60
        self.receiver_email = ""  # 1. Initialize an empty state for the receiver

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")

        grey_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        grey_frame_gau = cv2.GaussianBlur(grey_frame, (21, 21), 0)

        if self.first_frame is None:
            self.first_frame = grey_frame_gau
            return av.VideoFrame.from_ndarray(img, format="bgr24")

        delta_frame = cv2.absdiff(self.first_frame, grey_frame_gau)
        thresh_frame = cv2.threshold(delta_frame, 60, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
        contours, _ = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_detected = False

        for contour in contours:
            if cv2.contourArea(contour) < 5000:
                continue

            motion_detected = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        # 2. Check both motion AND if a receiver is actually defined
        if motion_detected and self.receiver_email:
            current_time = time.time()

            if (current_time - self.last_email_time) > self.cooldown:
                self.last_email_time = current_time

                success, buffer = cv2.imencode('.png', img)

                if success:
                    image_bytes = buffer.tobytes()
                    # 3. Pass the dynamic receiver email to the thread
                    email_thread = threading.Thread(
                        target=send_email,
                        args=(image_bytes, self.receiver_email)
                    )
                    email_thread.start()

        return av.VideoFrame.from_ndarray(img, format="bgr24")


# --- UI ARCHITECTURE ---

st.title("Live Motion Security Alert")
st.write(
    "This application monitors your webcam for movement and immediately emails a captured frame to the address provided below.")

# 4. Create the Input Block
user_email = st.text_input("Send Alert To:", placeholder="Enter your gmail address...")

# 5. Capture the WebRTC Context
ctx = webrtc_streamer(
    key="motion-detector",
    video_processor_factory=MotionProcessor,
    rtc_configuration={
        "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
    }
)

# 6. The Bridge: Push the Streamlit UI state into the WebRTC Thread
if ctx.video_processor:
    ctx.video_processor.receiver_email = user_email