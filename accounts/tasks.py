from celery import shared_task
from time import sleep
from core import settings
from django.core.mail import send_mail

@shared_task
def sendmail():
    send_mail(
            "bg proccess",
            "this is a short message",
            settings.EMAIL_HOST_USER,
            [
                "to@example.com",
            ],
        )
    print("email sended")