import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_reply_email(to_email, subject, reply_message):

    try:

        msg = MIMEMultipart()

        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = f"Re: {subject}"

        msg.attach(MIMEText(reply_message, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)

        server.starttls()

        server.login(
            EMAIL_ADDRESS,
            EMAIL_PASSWORD
        )

        server.sendmail(
            EMAIL_ADDRESS,
            to_email,
            msg.as_string()
        )

        server.quit()

        print("✅ Email sent successfully")

    except Exception as e:

        print("❌ Email send failed")
        print(e)