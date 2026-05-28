"""
JARVIS - Gmail Integratsiyasi
Email o'qish va yuborish
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class GmailModule:
    def __init__(self):
        self.email = os.getenv("GMAIL_ADDRESS", "")
        self.password = os.getenv("GMAIL_APP_PASSWORD", "")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
    
    def send_email(self, to_email, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain', 'utf-8'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email, self.password)
                server.send_message(msg)
            return f"✅ Email yuborildi: {to_email}"
        except Exception as e:
            return f"❌ Email yuborib bo'lmadi: {e}"
    
    def is_configured(self):
        return bool(self.email and self.password)
