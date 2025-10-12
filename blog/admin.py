from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from . models import Post, Category

# Register your models here.
class PostAdmin(MarkdownxModelAdmin):
    prepopulated_fields = {"slug": ["title"]}
    list_display = ['title', "slug", "created_at", "status"]
    search_fields = ['title', 'body']


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
