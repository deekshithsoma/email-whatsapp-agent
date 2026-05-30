import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Gmail credentials
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def send_reply_email(to_email, subject, reply_message):

    try:

        print("📧 Preparing reply email...")

        # Create email object
        msg = MIMEMultipart()

        msg["From"] = EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = f"Re: {subject}"

        # Add message body
        msg.attach(MIMEText(reply_message, "plain"))

        print("🔐 Connecting to Gmail SMTP...")

        # Connect to Gmail SMTP server
        server = smtplib.SMTP("smtp.gmail.com", 587)

        # Start TLS encryption
        server.starttls()

        print("✅ SMTP connection successful")

        # Login to Gmail
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        print("✅ Gmail login successful")

        # Send email
        server.sendmail(
            EMAIL_ADDRESS,
            to_email,
            msg.as_string()
        )

        print("✅ Reply email sent successfully")

        # Close server
        server.quit()

        print("✅ SMTP server closed")

    except Exception as e:

        print("❌ Failed to send email")
        print("Error:", e)


# Manual test
if __name__ == "__main__":

    print("🚀 Testing send_email.py")

    # Replace with your testing email
    test_email = "deekshithsoma@gmail.com"

    send_reply_email(
        test_email,
        "Test Subject",
        "Hello from WhatsApp Email Agent"
    )