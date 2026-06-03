from celery import shared_task
from time import sleep
from core.settings import deployment
from django.core.mail import send_mail

@shared_task
def sendmail():
    send_mail(
            "bg proccess",
            "this is a short message",
            deployment.EMAIL_HOST_USER,
            [
                "to@example.com",
            ],
        )
    print("email sended")


@shared_task
def sendـreset_password_email(user_email, reset_link, user_name):
    send_mail(
    subject="Password Reset Request",
    message=f"Click the link to reset your password: {reset_link}",
    from_email=deployment.DEFAULT_FROM_EMAIL,
    recipient_list=[user_email],
    fail_silently=False,
    html_message=f"""
    <html>
        <body>
            <p>Hello {user_name},</p>
            <p>We received a request to reset your password.</p>
            <p>
                <a href="{reset_link}">Click here to reset your password</a>
            </p>
            <p>This link is valid for 10 minutes.</p>
            <p>If you didn't request this, please ignore this email.</p>
        </body>
    </html>
    """
    )
    return f"send to {user_email}"
