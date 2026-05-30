from flask import Flask, request
from send_email import send_reply_email

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():

    # Receive WhatsApp message
    incoming_msg = request.form.get("Body", "").strip()

    print("\n📩 WhatsApp Reply Received")
    print("💬 Message:", incoming_msg)

    # Check reply format
    if incoming_msg.lower().startswith("reply:"):

        # Extract reply text
        reply_text = incoming_msg[6:].strip()

        print("✅ Reply Text:", reply_text)

        # Read latest sender email
        try:

            with open("latest_sender.txt", "r") as f:

                sender_email = f.read().strip()

            print("📧 Sending email reply to:", sender_email)

        except Exception as e:

            print("❌ Failed to read sender email")
            print(e)

            return "No sender email found"

        # Send email
        try:

            send_reply_email(
                sender_email,
                "WhatsApp Reply",
                reply_text
            )

            print("✅ Reply email sent successfully")

            return "Reply email sent successfully"

        except Exception as e:

            print("❌ Failed to send email")
            print(e)

            return "Email sending failed"

    else:

        print("⚠ Invalid reply format")

        return "Use format: reply: your message"


# Run Flask app
if __name__ == "__main__":

    app.run(port=5000)