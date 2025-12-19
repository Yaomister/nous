import os

from pydantic import EmailStr

from fastapi_mail import FastMail, ConnectionConfig, MessageSchema


BASE_DIR = os.path.dirname(os.path.abspath(__file__))



conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL"),
    MAIL_PASSWORD=os.getenv("EMAIL_APP_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.mail.yahoo.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER=os.path.join(BASE_DIR, "templates"),
)

fast_mail = FastMail(conf)


async def send_reset_email(email: EmailStr, reset_url: str):
    message = MessageSchema(subject="Reset your password", recipients=[email], template_body={"user_email" : email, "reset_url" : reset_url}, subtype="html")

    await fast_mail.send_message(
        message= message,
        template_name="reset_password.html"
    )
