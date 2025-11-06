# app/server/emailing.py
from dotenv import load_dotenv
load_dotenv()

import os, smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

SENDER_EMAIL = os.getenv("SENDER_EMAIL", "support@uptrendhunter.com")
SENDER_NAME  = os.getenv("SENDER_NAME",  "Uptrend Hunter")
SMTP_HOST    = os.getenv("SMTP_HOST",    "mail.privateemail.com")
SMTP_PORT    = int(os.getenv("SMTP_PORT", "465"))
SMTP_PASS    = os.getenv("SMTP_PASS")
SMTP_USER    = os.getenv("SMTP_USER", SENDER_EMAIL)

def _send_text(to_email: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr((SENDER_NAME, SENDER_EMAIL))
    msg["To"] = to_email

    # Önce SSL 465 dene, olmazsa 587 STARTTLS
    try:
        with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT, timeout=20) as s:
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)
    except Exception:
        with smtplib.SMTP(SMTP_HOST, 587, timeout=20) as s:
            s.ehlo(); s.starttls(); s.ehlo()
            s.login(SMTP_USER, SMTP_PASS)
            s.send_message(msg)

def send_welcome_email(to_email: str, name: str = ""):
    subject = "Welcome to Uptrend Hunter — Your account is ready 🚀"
    body = f"""Hi there,

Your Uptrend Hunter account has been created successfully.

You can log in and start exploring rising Amazon search trends.
Dashboard: https://www.uptrendhunter.com/app

Plan: Starter (demo limits apply)
• Up to 6 weeks lookback
• Top 50 results per query

Need help? Just reply to this email or write to support@uptrendhunter.com.


— Uptrend Hunter Team
Built by Amazon sellers, for Amazon sellers.
"""
    _send_text(to_email, subject, body)

def send_pro_activated_email(to_email: str, name: str = ""):
    subject = "Uptrend Hunter Pro — Activated ✅"
    body = f"""Hi there,

Your Uptrend Hunter Pro plan is now active. 🎉

What you’ve unlocked:
• Full 24+ week history
• Up to 250 results per query
• Advanced include/exclude filters
• Priority updates & support

Open your dashboard: https://www.uptrendhunter.com/app

If you have any questions, reply to this email or contact support@uptrendhunter.com.
— The Uptrend Hunter Team
Built by Amazon sellers, for Amazon sellers.
"""
    _send_text(to_email, subject, body)
