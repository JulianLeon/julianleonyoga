from .base import *
import os

# Laden der kritischen Secrets mit einem Fallback-Wert,
# um String-Verkettungs-Fehler beim Start zu vermeiden.
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'default-django-key')

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 

DEBUG = False

# Stelle sicher, dass Anymail in der Produktion geladen wird
INSTALLED_APPS += ['anymail']

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

# Brevo API Key aus Umgebungsvariable laden (mit Fallback)
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "dummy-brevo-key") 

ANYMAIL = {
    # Anymail verwendet diesen Schlüssel für die API-Authentifizierung
    "BREVO_API_KEY": BREVO_API_KEY,
}

# Absenderadresse wird als eigenständige Umgebungsvariable gesetzt (MUSS in Brevo verifiziert sein!)
# Dies ist die sauberste Methode.
DEFAULT_FROM_EMAIL = os.getenv("ADMIN_EMAIL", "julian.sagberger@gmail.com")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
#
## Ende E-Mail Settings
##


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
