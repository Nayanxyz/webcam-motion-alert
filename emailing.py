from email.message import EmailMessage
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv("GMAIL_PASSWORD")
SENDER = "nayan7857@gmail.com"
# RECEIVER is gone from here.

def send_email(image_bytes, receiver_email): # Added receiver_email parameter
    # Do not execute if the email is empty
    if not receiver_email:
        return

    email_message = EmailMessage()
    email_message["Subject"] = "Security Alert"
    email_message.set_content("Motion detected at the camera.")
    email_message.add_attachment(image_bytes, maintype="image", subtype="png")

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, receiver_email, email_message.as_string()) # Inject dynamic receiver
    gmail.quit()