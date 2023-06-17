from django.contrib import admin

from .models import JobseekerProfile


@admin.register(JobseekerProfile)
class JobseekerProfileAdmin(admin.ModelAdmin):
    '''Define admin model for JobseekerProfile model.'''

    list_display = ['user', 'name', 'gender', 'dob']
    list_filter = ['gender']
    search_fields = ['user__email', 'name']
