from django.core.paginator import Paginator, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect


from .forms import AllJobSearchForm
from .models import Job
from .helpers import (
    get_jobs_matching_get_params, raw_query_string_parameters)

PAGINATION_AMOUNT = 25


def home(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/home.html', {'jobs': jobs})


def about(request):
    return render(request, 'jobs/about.html')


def all_jobs(request, page=1):
    job_list = get_jobs_matching_get_params(request)
    search_form = AllJobSearchForm(initial=request.GET)
    paginator = Paginator(job_list, PAGINATION_AMOUNT)
    try:
        jobs = paginator.page(page)
    except EmptyPage:
        # ha nincs ilyen oldal, akkor az utolso ervenyes oldalra redirect
        response = redirect(
            reverse('jobs:all_jobs', args=(paginator.num_pages,)))
        response['Location'] += raw_query_string_parameters(request)
        return response
    return render(
        request,
        'jobs/all_jobs.html',
        {
            'jobs': jobs,
            'search_form': search_form,
            'query_string': raw_query_string_parameters(request)
        })


def specific_job(request, id_num):
    job = get_object_or_404(Job, pk=id_num)
    return render(request, 'jobs/specific_job.html', {'job': job})
