from django.contrib import admin
from .models import Blog, SiteSettings

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at')

admin.site.register(Blog, BlogAdmin)

admin.site.register(SiteSettings)