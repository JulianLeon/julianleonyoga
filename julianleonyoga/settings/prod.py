from .base import *
import os

# Laden der kritischen Secrets mit einem Fallback-Wert,
# um String-Verkettungs-Fehler beim Start zu vermeiden.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-django-key')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 

DEBUG = True



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
EMAIL_BACKEND = "anymail.backends.brevo.EmailBackend"


ANYMAIL = {
    "BREVO_API_KEY": os.getenv("BREVO_API_KEY"),
}

DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "julian.sagberger@gmail.com")



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
