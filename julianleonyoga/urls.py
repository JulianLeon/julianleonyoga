from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.sitemaps.views import sitemap
from base.sitemaps import HomeSitemap
from base.views import save_cookie_consent
from django.views.generic.base import TemplateView

from blog.views import CloudinaryImageUploadView

sitemaps = {
    "static": HomeSitemap(),
}

urlpatterns = [
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path("__reload__/", include("django_browser_reload.urls")),
    path('', include('base.urls')),
    # path('blog/', include('blog.urls')),
    path('admin/', admin.site.urls),
    # Überschreibe die Standard-Upload-URL
    path('markdownx/upload/', CloudinaryImageUploadView.as_view(), name='markdownx_upload'),
    # Füge alle anderen markdownx URLs hinzu
    path('markdownx/', include('markdownx.urls')),
    path('api/cookie-consent/', save_cookie_consent, name='cookie_consent'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
