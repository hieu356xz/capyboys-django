from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "last_name", "username", "is_superuser", "is_staff", "is_active"]
    list_filter = ["is_superuser", "is_staff", "is_active"]
    search_fields = ["email", "first_name", "last_name", "username"]

admin.site.register(User, UserAdmin)
