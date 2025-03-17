from django.contrib import admin
from .models import Collection, BookCollection

class CollectionBookInline(admin.TabularInline):
    model = BookCollection
    extra = 1

class CollectionAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

    inlines = [CollectionBookInline]

admin.site.register(Collection, CollectionAdmin)
