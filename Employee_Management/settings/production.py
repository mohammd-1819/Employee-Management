import os
from .base import *
import dj_database_url

ALLOWED_HOSTS = ['*']

DEBUG = False

DATABASES = {

    'default': dj_database_url.config(default=os.environ.get('POSTGRESQL_DATABASE_URL'))
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
