from django.contrib import admin

from .models import Resume


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    '''Define admin model for Resume model.'''

    list_display = ['jobseeker', 'occupation', 'skills']
    search_fields = ['jobseeker__email', 'occupation', 'skills']
