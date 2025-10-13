from django.urls import path
from . import views
from django.views.generic.base import TemplateView

app_name = 'base'

urlpatterns = [
    path('', views.home, name='home'),
    path('robots.txt', TemplateView.as_view(template_name='base/robots.txt', content_type='text/plain')),
    path('impressum/', views.impressum, name='impressum'),
    path('datenschutz/', views.datenschutz, name='datenschutz'),
]