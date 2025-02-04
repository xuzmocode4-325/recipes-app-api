"""
Django admin customisation
"""

from django.contrib import admin 
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


from . models import User

class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users"""
    ordering = ['id']
    list_display = ['name', 'email']

admin.site.register(User, UserAdmin)