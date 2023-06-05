from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    '''Define admin model for custom User model with no username field.'''

    # The fields which displayed on "Change User" page in admin panel
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    # The fields which displayed on "Add User" page in admin panel
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'role', 'password1', 'password2')
            }
        ),
    )

    # The fields which displayed on "Users" page in admin panel
    list_display = ('email', 'name', 'role', 'is_staff', 'last_login')
    # list of fields to generate filters in the right sidebar of admin panel
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'groups')
    # Search fields to search in the search bar in the top of admin panel
    search_fields = ('email',)
    # Default ordering in admin panel
    ordering = ('email',)

    filter_horizontal = ('groups', 'user_permissions',)
