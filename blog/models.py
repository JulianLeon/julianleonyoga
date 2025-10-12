from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
from datetime import datetime, date
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify as default_markdownify
from blog.utils.markdown_utils import markdownify



# Create your models here.

## Category Model
class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(unique=True)
   

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={
            "category_slug": self.slug,
        })


## Post Model
class Post(models.Model):

    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    title = models.CharField(max_length=60)
    slug = models.SlugField(unique=True)
    header_image = models.ImageField(upload_to='images/')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    snippet = models.TextField(max_length=255)
    meta_description = models.TextField(max_length=158)
    body = MarkdownxField()
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title
    
    @property
    def formatted_content(self):
        """Gibt den als HTML formatierten Inhalt zurück"""
        return markdownify(self.body)

   

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={
            "slug": self.slug,
        })