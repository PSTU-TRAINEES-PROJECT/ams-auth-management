import aiosmtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import get_config


async def send_verification_email(email: str, token: str):
    config = get_config()
    verification_url = f"{config.frontend_url}/verify-email?token={token}"
    
    message = MIMEMultipart()
    message["From"] = config.smtp_user
    message["To"] = email
    message["Subject"] = "Email Verification"

    body = f"""
    Hi,

    Please click the link below to verify your email address:
    
    {verification_url}
    
    If you did not request this, please ignore this email.

    Thanks,
    AMS Team
    """

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
