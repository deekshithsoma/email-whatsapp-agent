from flask import Flask, request
from send_email import send_reply_email
import os

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h2>✅ Email WhatsApp Agent Running</h2>
    <p>Webhook is active.</p>
    """


@app.route("/webhook", methods=["POST"])
def webhook():

    incoming_msg = request.form.get("Body", "").strip()

    print("\n📩 WhatsApp Reply Received")
    print("💬 Message:", incoming_msg)

    if incoming_msg.lower().startswith("reply:"):

        reply_text = incoming_msg[6:].strip()

        print("✅ Reply Text:", reply_text)

        try:

            with open("latest_sender.txt", "r") as f:
                sender_email = f.read().strip()

            print("📧 Sending email reply to:", sender_email)

        except Exception as e:

            print("❌ Failed to read latest_sender.txt")
            print(e)

            return "No sender email found", 400

        try:

            send_reply_email(
                sender_email,
                "WhatsApp Reply",
                reply_text
            )

            print("✅ Reply email sent successfully")

            return "Reply email sent successfully", 200

        except Exception as e:

            print("❌ Failed to send email")
            print(e)

            return "Email sending failed", 500

    print("⚠ Invalid reply format")

    return "Use format: reply: your message", 200


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )