import os
import smtplib
from email.mime.text import MIMEText


def send_email(subject: str, body: str) -> None:
    gmail_address = os.environ["GMAIL_ADDRESS"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]
    recipients = [
        addr.strip()
        for addr in os.environ["RECIPIENT_EMAILS"].split(",")
        if addr.strip()
    ]

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = f"JTK Lunsjbot <{gmail_address}>"
    msg["To"] = ", ".join(recipients)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(gmail_address, app_password)
        server.sendmail(gmail_address, recipients, msg.as_string())


if __name__ == "__main__":
    from dotenv import load_dotenv

    load_dotenv()
    send_email("Test fra JTK Lunsjbot", "Hvis du ser denne, funker e-postutsendelsen.")