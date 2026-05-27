# settings/deployment.py
from .base import * 


DEBUG = True
SECRET_KEY = "SECRET_KEY"
ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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