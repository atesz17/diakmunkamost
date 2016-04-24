from django.contrib import admin

from .models import Job, JobType, JobProvider


class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'job_type', 'min_salary')
    list_filter = ('job_type',)
    ordering = ('title',)
    search_fields = ('title',)

admin.site.register(Job, JobAdmin)
admin.site.register(JobType)
admin.site.register(JobProvider)
