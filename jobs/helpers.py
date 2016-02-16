from django.db.models import Q

from jobs.models import Job

import urllib


def get_jobs_matching_get_params(request):
    #  Csunya TODO
    jobs = Job.objects.all()
    if "min_salary" in request.GET and request.GET['min_salary'] != "":
        try:
            value = int(request.GET['min_salary'])
            jobs = Job.objects.filter(min_salary__gte=value)
        except ValueError:
            pass
    if "job_types" in request.GET:
        conditions = Q()
        for job_type in request.GET.copy().pop('job_types'):
            try:
                value = int(job_type)
                conditions = conditions | Q(job_type=job_type)
            except ValueError:
                pass
        jobs = jobs.filter(conditions)
    if "order_by" in request.GET and int(request.GET['order_by']) == 0:
        jobs = jobs.order_by('min_salary')
    else:
        jobs = jobs.order_by('-min_salary')
    return jobs


def raw_query_string_parameters(request):
    if urllib.parse.urlencode(request.GET) != "":
        return '?' + urllib.parse.urlencode(request.GET)
    return ""
