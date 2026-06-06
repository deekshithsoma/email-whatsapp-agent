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

# Validate WhatsApp format
if not YOUR_WHATSAPP.startswith("whatsapp:"):
    YOUR_WHATSAPP = "whatsapp:" + YOUR_WHATSAPP

client = Client(TWILIO_SID, TWILIO_TOKEN)

spam_keywords = [
    "no-reply", "noreply", "newsletter", "promotion",
    "offer", "sale", "discount", "otp", "verification",
    "linkedin", "facebook", "instagram", "twitter",
    "alert", "notification", "updates", "marketing",
    "unsubscribe"
]

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

        # Filter emails
        for e_id in email_ids:
            try:
                status, msg_data = mail.fetch(e_id, "(RFC822)")
                raw_email = msg_data[0][1]

                msg = email.message_from_bytes(raw_email)

                sender = str(msg.get("from", "")).lower()
                subject = str(msg.get("subject", "")).lower()

                ignore = any(word in sender or word in subject for word in spam_keywords)

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

                sender_name, sender_email = parseaddr(str(msg.get("from", "")))

                body = ""

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True)
                            if body:
                                body = body.decode(errors="ignore")
                                break
                else:
                    body = msg.get_payload(decode=True)
                    if body:
                        body = body.decode(errors="ignore")

                body = body.strip() if body else "No message content"

                # IMPORTANT FIX: safe limit for Twilio
                MAX_LEN = 800
                if len(body) > MAX_LEN:
                    body = body[:MAX_LEN] + "\n\n...truncated..."

                message_text = f"""
📩 IMPORTANT EMAIL

👤 From: {sender_email}
📝 Subject: {subject}

💬 Message:
{body}

-----------------------
Reply using:
reply: your message
"""

                print("📤 Sending to WhatsApp...")

                message = client.messages.create(
                    from_="whatsapp:+14155238886",
                    body=message_text,
                    to=YOUR_WHATSAPP
                )

                print("✅ Sent to WhatsApp")
                print("SID:", message.sid)

                # mark email as seen (prevents duplicates)
                mail.store(e_id, '+FLAGS', '\\Seen')

            except Exception as e:
                print("❌ WhatsApp Send Error:")
                print(e)

        mail.logout()

    except Exception as e:
        print("❌ Main Error:")
        print(e)

    print("⏳ Waiting 30 seconds...")
    time.sleep(30)