import os

from .base import *

# Debug
DEBUG = False

CSRF_TRUSTED_ORIGINS = ["https://qabul-api.xiuedu.uz", "https://www.qabul-api.xiuedu.uz"]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT', ''),
    }
}
