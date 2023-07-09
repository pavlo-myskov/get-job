from django.contrib import admin

from .models import EmployerProfile


@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    '''Define admin model for EmployerProfile model.'''

    list_display = ['user', 'name', 'company']
    search_fields = ['user__email', 'name', 'company']
