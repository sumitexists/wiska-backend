from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AnonymousAlias, User


class CustomUserAdmin(UserAdmin):
    # 1. This adds your custom fields to the "Add User" screen
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Wiska Details', {
            'fields': ('phone_number', 'email','first_name', 'last_name'),
        }),
    )
    
    # 2. This adds your custom fields to the "Edit User" screen

# Register the User using your newly upgraded CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

# Register the mask normally
admin.site.register(AnonymousAlias)