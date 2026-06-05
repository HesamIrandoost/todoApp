# accounts/signals.py

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """
    این سیگنال به محض ایجاد یک کاربر جدید، یک توکن احراز هویت برای او می‌سازد.
    """
    if created:
        Token.objects.create(user=instance)
        # اختیاری: می‌توانید یک لاگ یا کار دیگر هم در اینجا انجام دهید.
        # print(f"Token created for user: {instance.email}")