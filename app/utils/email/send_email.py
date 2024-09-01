import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.templates.email_verification_template import VERIFICATION_EMAIL_TEMPLATE
from config import get_config


async def send_verification_email(email: str, token: str):
    config = get_config()
    verification_url = f"{config.frontend_url}/verify-email?token={token}"
    
    message = MIMEMultipart()
    message["From"] = config.smtp_user
    message["To"] = email
    message["Subject"] = "Email Verification"

    body = VERIFICATION_EMAIL_TEMPLATE.format(verification_url=verification_url)

    message.attach(MIMEText(body, "plain"))
    
    print("Sending verification email...")
    await aiosmtplib.send(
        message,
        hostname=config.smtp_server,
        port=config.smtp_port,
        username=config.smtp_user,
        password=config.smtp_password,
        start_tls=True,
        
    )
