from django.urls import include, path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog, name='index'),
    path('search/', views.search, name='search'),
    path('categories/<str:category_slug>', views.category, name='category'),
    path('posts/<str:slug>', views.post_detail, name='post_detail'),
    # Überschreibe die Standard-Upload-URL
    path('markdownx/upload/', views.CloudinaryImageUploadView.as_view(), name='markdownx_upload'),
]