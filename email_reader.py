import imaplib
import email
from twilio.rest import Client
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Gmail credentials
EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")

# Twilio credentials
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
YOUR_WHATSAPP = os.getenv("YOUR_WHATSAPP_NUMBER")

# Spam/promotional keywords
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

print("🚀 Email → WhatsApp Agent Started")

# Infinite loop
while True:

    try:

        print("\n🔄 Checking for new emails...")

        # Connect Gmail
        mail = imaplib.IMAP4_SSL("imap.gmail.com")

        mail.login(EMAIL, PASSWORD)

        print("✅ Gmail login successful")

        # Open inbox
        mail.select("inbox")

        # Search unread emails
        status, messages = mail.search(None, '(UNSEEN)')

        email_ids = messages[0].split()

        print(f"📨 Total unread emails found: {len(email_ids)}")

        # No unread emails
        if len(email_ids) == 0:

            print("📭 No unread emails")

            mail.logout()

            print("⏳ Waiting 30 seconds...\n")

            time.sleep(30)

            continue

        filtered_email_ids = []

        # Filter emails
        for e_id in email_ids:

            try:

                status, msg_data = mail.fetch(e_id, "(RFC822)")

                raw_email = msg_data[0][1]

                msg = email.message_from_bytes(raw_email)

                sender = str(msg["from"]).lower()

                subject = str(msg["subject"]).lower()

                print("\n------------------------------")
                print("📧 Checking Email")
                print("👤 From:", sender)
                print("📝 Subject:", subject)

                ignore = False

                # Ignore spam/promotions
                for word in spam_keywords:

                    if word in sender or word in subject:

                        ignore = True

                        print("🚫 Ignored spam/promotional email")

                        break

                # Important email
                if not ignore:

                    filtered_email_ids.append(e_id)

                    print("✅ Important email selected")

            except Exception as e:

                print("❌ Error reading email")
                print(e)

        # Read latest important email only
        filtered_email_ids = filtered_email_ids[-1:]

        # No important emails
        if len(filtered_email_ids) == 0:

            print("\n📭 No important unread emails found")

            mail.logout()

            print("⏳ Waiting 30 seconds...\n")

            time.sleep(30)

            continue

        # Twilio client
        client = Client(TWILIO_SID, TWILIO_TOKEN)

        # Process email
        for e_id in filtered_email_ids:

            try:

                status, msg_data = mail.fetch(e_id, "(RFC822)")

                raw_email = msg_data[0][1]

                msg = email.message_from_bytes(raw_email)

                subject = msg["subject"]

                sender = msg["from"]

                # Save latest sender email
                with open("latest_sender.txt", "w") as f:

                    f.write(sender)

                body = ""

                # Extract body
                if msg.is_multipart():

                    for part in msg.walk():

                        if part.get_content_type() == "text/plain":

                            try:

                                body = part.get_payload(decode=True).decode()

                                break

                            except:

                                body = "Unable to decode body"

                else:

                    try:

                        body = msg.get_payload(decode=True).decode()

                    except:

                        body = "Unable to decode body"

                # Clean body
                body = body.strip()

                # Limit WhatsApp message length
                MAX_LENGTH = 1200

                if len(body) > MAX_LENGTH:

                    body = body[:MAX_LENGTH]

                    body += "\n\n...Message truncated..."

                # WhatsApp message
                whatsapp_message = f"""
📩 IMPORTANT EMAIL

FROM_EMAIL: {sender}

📝 Subject:
{subject}

💬 Message:
{body}

------------------------

Reply using:

reply: your message
"""

                print("\n📤 Sending to WhatsApp...")

                # Send WhatsApp
                message = client.messages.create(

                    from_='whatsapp:+14155238886',

                    body=whatsapp_message,

                    to=YOUR_WHATSAPP
                )

                print("✅ Sent to WhatsApp")

                print("📨 Message SID:", message.sid)

            except Exception as e:

                print("❌ Failed sending WhatsApp message")

                print(e)

        # Logout Gmail
        mail.logout()

    except Exception as e:

        print("❌ Main Error")
        print(e)

    # Wait before checking again
    print("\n⏳ Waiting 30 seconds before next check...\n")

    time.sleep(30)