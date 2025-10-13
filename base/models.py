from django.db import models

# Create your models here.

from django.db import models
from django.utils import timezone

class CookieConsent(models.Model):
    """Speichert Cookie-Zustimmungen der Besucher"""
    
    session_key = models.CharField(max_length=255, unique=True)
    analytics_consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Cookie Zustimmung"
        verbose_name_plural = "Cookie Zustimmungen"
    
    def __str__(self):
        return f"Consent {self.session_key[:8]}..."

