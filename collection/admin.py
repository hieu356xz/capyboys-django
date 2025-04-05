from django.contrib import admin
from django.template.defaultfilters import slugify
from unidecode import unidecode
from .models import Collection, BookCollection

class CollectionBookInline(admin.TabularInline):
    model = BookCollection
    extra = 1

    autocomplete_fields =  ('book',)
class CollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

    inlines = [CollectionBookInline]

    def save_model(self, request, obj, form, change):
        if 'slug' not in form.changed_data or not change:
            obj.slug = slugify(unidecode(obj.name))
        return super().save_model(request, obj, form, change)

admin.site.register(Collection, CollectionAdmin)
