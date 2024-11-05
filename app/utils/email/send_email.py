from utils.templates.email_verification_template import VERIFICATION_EMAIL_TEMPLATE
from config import get_config
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

config = get_config()

# Create a brevo API configuration
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = config.brevo_api_key
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))


async def send_verification_email(username: str, email: str, token: str):
    
    verification_url = f"{config.frontend_url}/verify-email?token={token}"
    
    sender = {"name": "AMS", "email": config.email_sender}
    subject = "Email Verification From AMS"
    to = [{"email": email, "name": username}]

    body = VERIFICATION_EMAIL_TEMPLATE.replace("{{verification_url}}", verification_url).replace("{{user_name}}", username)
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=body, sender=sender, subject=subject)
    
    try:
        api_response = api_instance.send_transac_email(send_smtp_email)
        print("Email sent successfully!")
        return
    except ApiException as e:
        print(f"Error sending email: {e}")
        return

