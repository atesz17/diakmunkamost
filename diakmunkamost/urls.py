from django.conf.urls import url, include
from django.contrib import admin

from jobs import views as job_views

urlpatterns = [
    url(r'^$', job_views.home, name='home'),
    url(r'^kapcsolat/$', job_views.about, name='about'),
    url(r'^munkak/', include('jobs.urls')),
    url(r'^admin/', admin.site.urls),
]
