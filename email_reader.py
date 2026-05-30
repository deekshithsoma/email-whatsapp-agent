import imaplib
import email
from email.utils import parseaddr
from twilio.rest import Client
from dotenv import load_dotenv
import os
import time

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
YOUR_WHATSAPP = os.getenv("YOUR_WHATSAPP_NUMBER")

spam_keywords = [
    "no-reply",
    "noreply",
    "newsletter",
    "promotion",
    "offer",
    "sale",
    "discount",
    "otp",
    "verification",
    "linkedin",
    "facebook",
    "instagram",
    "twitter",
    "alert",
    "notification",
    "updates",
    "marketing",
    "unsubscribe"
]

client = Client(TWILIO_SID, TWILIO_TOKEN)

print("🚀 Email → WhatsApp Agent Started")

while True:

    try:

        print("\n🔄 Checking for new emails...")

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(EMAIL, PASSWORD)

        mail.select("inbox")

        status, messages = mail.search(None, '(UNSEEN)')

        email_ids = messages[0].split()

        print(f"📨 Unread Emails: {len(email_ids)}")

        if not email_ids:

            mail.logout()
            time.sleep(30)
            continue

        important_emails = []

        for e_id in email_ids:

            try:

                status, msg_data = mail.fetch(e_id, "(RFC822)")

                raw_email = msg_data[0][1]

                msg = email.message_from_bytes(raw_email)

                sender = str(msg.get("from", "")).lower()
                subject = str(msg.get("subject", "")).lower()

                ignore = False

                for word in spam_keywords:

                    if word in sender or word in subject:
                        ignore = True
                        break

                if not ignore:
                    important_emails.append(e_id)

            except Exception as e:
                print("❌ Email Read Error:", e)

        important_emails = important_emails[-1:]

        if not important_emails:

            print("📭 No important emails")
            mail.logout()
            time.sleep(30)
            continue

        for e_id in important_emails:

            try:

                status, msg_data = mail.fetch(e_id, "(RFC822)")

                raw_email = msg_data[0][1]

                msg = email.message_from_bytes(raw_email)

                subject = str(msg.get("subject", "No Subject"))

                sender_name, sender_email = parseaddr(
                    str(msg.get("from", ""))
                )

                body = ""

                if msg.is_multipart():

                    for part in msg.walk():

                        if part.get_content_type() == "text/plain":

                            try:

                                body = part.get_payload(
                                    decode=True
                                ).decode(errors="ignore")

                                break

                            except:
                                pass

                else:

                    try:

                        body = msg.get_payload(
                            decode=True
                        ).decode(errors="ignore")

                    except:
                        pass

                body = body.strip()

                if not body:
                    body = "No message content"

                if len(body) > 1200:

                    body = body[:1200]
                    body += "\n\n...Message truncated..."

                with open(
                    "latest_sender.txt",
                    "w",
                    encoding="utf-8"
                ) as f:

                    f.write(sender_email + "\n")
                    f.write(subject + "\n")

                whatsapp_message = f"""
📩 IMPORTANT EMAIL

👤 From:
{sender_email}

📝 Subject:
{subject}

💬 Message:
{body}

-----------------------

Reply using:

reply: your message
"""

                message = client.messages.create(
                    from_="whatsapp:+14155238886",
                    body=whatsapp_message,
                    to=YOUR_WHATSAPP
                )

                print("✅ Sent to WhatsApp")
                print("SID:", message.sid)

            except Exception as e:

                print("❌ WhatsApp Send Error")
                print(e)

        mail.logout()

    except Exception as e:

        print("❌ Main Error")
        print(e)

    print("⏳ Waiting 30 seconds...")
    time.sleep(30)
