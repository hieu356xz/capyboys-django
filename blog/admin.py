from django.contrib import admin
from django.template.defaultfilters import slugify
from .models import Blog, BlogType

class BlogTypeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        if 'slug' not in form.changed_data or not change:
            obj.slug = slugify(obj.name)
        return super().save_model(request, obj, form, change)


class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'content', 'description']
    list_filter = ['blog_type']

    autocomplete_fields = ('blog_type',)

    def save_model(self, request, obj, form, change):
        if 'slug' not in form.changed_data or not change:
            obj.slug = slugify(obj.title)
        return super().save_model(request, obj, form, change)


admin.site.register(Blog, BlogAdmin)
admin.site.register(BlogType, BlogTypeAdmin)