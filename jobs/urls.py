from django.conf.urls import url

from . import views

app_name = 'jobs'
urlpatterns = [
    url(r'^oldal/(?P<page>\d+)/$', views.all_jobs, name='all_jobs'),
    url(r'^(?P<id_num>\d+)/$', views.specific_job, name='specific_job')
]
