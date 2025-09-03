# SMTP sender (MailHog/Gmail/Outlook)
import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

SMTP_HOST = os.getenv("SMTP_HOST", "mailhog")
SMTP_PORT = int(os.getenv("SMTP_PORT", "1025"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM = os.getenv("SMTP_FROM", "Sales <sales@example.com>")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "false").lower() == "true"

def send_email(to_email: str, subject: str, body: str):
    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = SMTP_FROM
    msg["To"] = to_email

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30) as server:
        if SMTP_USER and SMTP_PASSWORD:
            if SMTP_USE_TLS:
                server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
        server.sendmail(formataddr(("", SMTP_FROM)), [to_email], msg.as_string())
