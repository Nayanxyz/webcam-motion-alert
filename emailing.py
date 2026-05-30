from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv("GMAIL_PASSWORD")
SENDER = "nayan7857@gmail.com"
RECEIVER = "nayanxyz0@gmail.com"

def send_email(image_bytes):
    email_message = EmailMessage()
    email_message["Subject"] = "Security Alert"
    email_message.set_content("Motion detected at the camera.")

    # We no longer open a file. We just attach the raw bytes directly in memory.
    email_message.add_attachment(image_bytes, maintype="image", subtype="png")

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()