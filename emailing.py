from email.message import EmailMessage
import smtplib                                                          # smtplib /for sending emails by connecting to an SMTP or ESMTP server.
                                                                        # It supports sending plain-text, HTML, and multipart messages with attachments,
                                                                        # typically requiring a secure connection via SMTP_SSL or starttls()

import imghdr                                                                   # imghdr / a lightweight Python standard library module used to identify
import os                                                                       # the file format of an image by examining the
from dotenv import load_dotenv                                                   # first few bytes (the header) of a file or byte stream


load_dotenv()
PASSWORD = os.getenv("GMAIL_PASSWORD")
SENDER = "nayan7857@gmail.com"
RECEIVER = "nayanxyz0@gmail.com"


def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Security Alert"
    email_message.set_content("someone has arrived at the door")

    with open(image_path, "rb") as file:                             # read file as binary
        content = file.read()
    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()                                                         # It is the initial handshake that introduces the client to the server .
                                                                         # It is crucial for establishing a secure connection before providing credentials

    gmail.starttls()                                                     #to upgrade an insecure SMTP connection to a secure one using Transport Layer Security (TLS).
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path="images/53.png")

