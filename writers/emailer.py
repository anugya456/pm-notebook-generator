import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(attachment_path="weekly_report.md"):
    sender = os.getenv("EMAIL_FROM")
    recipient = os.getenv("EMAIL_TO")
    password = os.getenv("EMAIL_PASSWORD")

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Set up email
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = f"✅ PM Notebook Generated – {now}"

    body = f"Hi A,\n\nYour weekly PM report was generated successfully on {now}.\n\nThe Markdown file is attached.\n\n– Your bot"
    msg.attach(MIMEText(body, 'plain'))

    # Attach file
    if os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f'attachment; filename="{os.path.basename(attachment_path)}"')
        msg.attach(part)
    else:
        print(f"⚠️ Attachment not found: {attachment_path}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        print("✅ Email with attachment sent.")
    except Exception as e:
        print("❌ Failed to send email:", e)
