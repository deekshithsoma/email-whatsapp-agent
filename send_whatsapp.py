from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)

message = client.messages.create(
    from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
    body="New Email Received",
    to=os.getenv("YOUR_WHATSAPP_NUMBER")
)

print(message.sid)