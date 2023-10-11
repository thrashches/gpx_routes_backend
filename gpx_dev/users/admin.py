from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User

class UserAdmin(BaseUserAdmin):
    list_display = ['id', 'email', 'nickname', 'is_active', 'date_joined']
    list_display_links = ['email', 'nickname']
    ordering = ["date_joined"]


admin.site.register(User, UserAdmin)

