from django.contrib import admin
from .models import Blog, SiteSettings


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status', 'created_at')
    list_filter = ('status',)

admin.site.register(Blog, BlogAdmin)

admin.site.register(SiteSettings)