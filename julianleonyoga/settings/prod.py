from .base import *
import os

# Laden der kritischen Secrets mit einem Fallback-Wert,
# um String-Verkettungs-Fehler beim Start zu vermeiden.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-django-key')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 

DEBUG = False



ALLOWED_HOSTS = [
    '.railway.app',
    'julianleonyoga.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://hiddengem-production.up.railway.app', 
    'https://*.railway.app',
    'https://julianleonyoga.com',
]

##
## E-MAIL SETTINGS (Brevo über Anymail - Dauerhaft kostenlos)
##
# Das Backend wird auf Brevo umgestellt.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv('ADMIN_EMAIL') # This should be set in your .env file

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD') # This should be set in your .env file

ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')



DATABASE_URL = os.getenv("DATABASE_URL")
import dj_database_url
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.config(
            default=DATABASE_URL,
        )
    }

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
