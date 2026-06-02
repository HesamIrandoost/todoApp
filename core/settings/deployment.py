# settings/deployment.py
from .base import * 


DEBUG = True
SECRET_KEY = "zczczsx"
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

CORS_ALLOW_ALL_ORIGINS = True
# settings.py

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
STATIC_URL = 'static/'

# ✅ در توسعه از STATICFILES_DIRS استفاده می‌شود
STATICFILES_DIRS = [
    BASE_DIR / "static",  # پوشه استاتیک اصلی شما
]



# برای رفع خطای staticfiles
if not STATICFILES_DIRS[0].exists():

    STATICFILES_DIRS[0].mkdir(parents=True, exist_ok=True)


# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_HOST = 'smtp4dev'
# EMAIL_HOST = '127.0.0.1'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 25
DEFAULT_FROM_EMAIL = 'admin@admin.com'




CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://redis:6379/0')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Tehran'


# CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
