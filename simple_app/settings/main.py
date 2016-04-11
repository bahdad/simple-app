"""Django PRODUCTION settings for simple_app project."""
from os import environ

from simple_app.settings import *


DEBUG = False

SECRET_KEY = environ.get('SECRET_KEY', SECRET_KEY)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': '12345',
        # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP
        'HOST': '',
        # Empty string for default 5432
        'PORT': '',
    }
}
