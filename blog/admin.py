from django.contrib import admin
from .models import Blog, BlogType

class BlogTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content', 'description']
    list_filter = ['blog_type']

admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogType, BlogTypeAdmin)