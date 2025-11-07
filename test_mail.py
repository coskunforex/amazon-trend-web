import os
from app.server.emailing import send_welcome_email
from dotenv import load_dotenv
load_dotenv()

print("SENDER_EMAIL:", os.getenv("SENDER_EMAIL"))
print("SMTP_HOST:", os.getenv("SMTP_HOST"))
print("SMTP_PORT:", os.getenv("SMTP_PORT"))
pw = os.getenv("SMTP_PASS")
print("SMTP_PASS set mi?:", bool(pw), " | uzunluk:", len(pw) if pw else 0)

send_welcome_email("coskunforex@gmail.com", "Test User")
print("Mail gönderimi denendi.")
