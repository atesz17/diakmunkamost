from django.contrib import admin

from .models import Job, JobType, JobProvider

admin.site.register(Job)
admin.site.register(JobType)
admin.site.register(JobProvider)
