# settings/poduction.py
from .base import * 

from dotenv import load_dotenv
import os
load_dotenv()



# settings/deployment.py
from .base import * 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


DEBUG = False
SECRET_KEY = os.getenv("SECRET_KEY")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(',')


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# فایل‌های استاتیک در تولید
STATIC_ROOT = BASE_DIR / "staticfiles"

# رسانه‌ها (فایل‌های آپلودی)
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"