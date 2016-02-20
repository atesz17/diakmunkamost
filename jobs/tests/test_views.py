from django.core.paginator import Page
from django.core.urlresolvers import reverse
from django.db.models.query import QuerySet
from django.test import TestCase

from .helper import DummyJobManager
from jobs.models import Job
from jobs.views import PAGINATION_AMOUNT

import math
from unittest import skip


class HomePageTest(TestCase):
    """
    Kezdo oldallal kapcsolatos tesztek
    """

    def setUp(self):
        self.response = self.client.get(reverse('home'))
    """
    Altalanos tesztek
    """
    def test_home_page_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'jobs/home.html')

    def test_home_page_response_code_is_okay(self):
        self.assertEqual(self.response.status_code, 200)

    def test_home_page_has_correct_title(self):
        self.assertContains(self.response, '<title>Diákmunka most!</title>')

    @skip  # TODO: HTML elementek tesztelese
    def test_home_page_has_logo_pointing_to_home_(self):
        element = '<a class="navbar-brand" href="{0}">Diákmunka most!</a>'
        self.assertContains(self.response, element.format(reverse('home')))

    def test_home_page_has_link_to_about_page(self):
        element = '<a href="{0}">Az oldalról</a>'
        self.assertContains(self.response, element.format(reverse('about')))

    """
    Specifikus tesztek
    """
    @skip  # TODO: HTML elementek tesztelese
    def test_home_page_has_prim_btn_pointing_to_all_jobs(self):
        element = '<a type="button" class="btn btn-primary btn-lg" href="{0}">'
        self.assertContains(
            self.response,
            element.format(reverse('jobs:all_jobs', args=(1,))))

    def test_home_page_job_context_passed(self):
        self.assertIsInstance(self.response.context['jobs'], QuerySet)


class AboutPageTest(TestCase):
    """
    About page kapcsolatos tesztek
    """
    def setUp(self):
        self.response = self.client.get(reverse('about'))

    """
    Altalanos tesztek
    """
    def test_about_page_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'jobs/about.html')

    def test_about_page_response_code_is_okay(self):
        self.assertEqual(self.response.status_code, 200)

    def test_about_page_has_correct_title(self):
        element = '<title>Az oldalról | Diákmunka most!</title>'
        self.assertContains(self.response, element)

    @skip  # TODO: HTML elementek tesztelese
    def test_about_page_has_logo_pointing_to_home_(self):
        element = '<a class="navbar-brand" href="{0}">Diákmunka most!</a>'
        self.assertContains(self.response, element.format(reverse('home')))

    def test_about_page_has_link_to_about_page(self):
        element = '<a href="{0}">Az oldalról</a>'
        self.assertContains(self.response, element.format(reverse('about')))
    """
    Specifikus tesztek
    """


class AllJobPageTest(TestCase):

    fixtures = ['jobs.json']

    def setUp(self):
        self.non_existent_page = 1234
        self.job_count = 51

    def test_all_job_page_renders_correct_template(self):
        self.response = self.client.get(reverse(
            'jobs:all_jobs',
            args=(1,)))
        self.assertTemplateUsed(self.response, 'jobs/all_jobs.html')

    def test_all_job_page_response_code_is_okay(self):
        self.response = self.client.get(reverse(
            'jobs:all_jobs',
            args=(1,)))
        self.assertEqual(self.response.status_code, 200)

    def test_all_job_page_has_correct_title(self):
        self.response = self.client.get(reverse(
            'jobs:all_jobs',
            args=(1,)))
        self.assertContains(
            self.response,
            '<title>Összes Munka | Diákmunka most!</title>')

    def test_no_prev_link_on_first_page(self):
        self.response = self.client.get(reverse(
            'jobs:all_jobs',
            args=(1,)))
        self.assertNotContains(self.response, 'Előző')
        #  Ahhoz, hogy ez a teszt atmenjen, legalabb 2 oldalnyi munka kell
        self.assertContains(
            self.response,
            '<a href="{0}">{1}</a>'.format(
                reverse('jobs:all_jobs', args=(2,)), 'Következő'))

    def test_no_next_link_on_last_page(self):
        self.response = self.client.get(reverse(
            'jobs:all_jobs',
            args=(math.ceil(self.job_count/PAGINATION_AMOUNT),)
        ))
        self.assertNotContains(self.response, 'Következő')
        #  Ahhoz, hogy ez a teszt atmenjen, legalabb 2 oldalnyi munka kell
        self.assertContains(
            self.response,
            '<a href="{0}">{1}</a>'.format(
                reverse(
                    'jobs:all_jobs',
                    args=(math.ceil(self.job_count/PAGINATION_AMOUNT-1),)),
                'Előző'))

    def test_prev_and_next_links_are_visible_on_page(self):
        #  Ahhoz, hogy ez a teszt atmenjen, legalabb 3 oldalnyi munka kell
        self.response = self.client.get(reverse(
            'jobs:all_jobs', args=(2,)
        ))
        self.assertContains(
            self.response,
            '<a href="{0}">{1}</a>'.format(
                reverse(
                    'jobs:all_jobs',
                    args=(1,)),
                'Előző'))
        self.assertContains(
            self.response,
            '<a href="{0}">{1}</a>'.format(reverse(
                'jobs:all_jobs', args=(3,)),
                'Következő'))

    def test_non_existent_page_redirects_to_last_page(self):
        self.response = self.client.get(reverse(
            'jobs:all_jobs',
            args=(self.non_existent_page,)))
        self.assertRedirects(
            self.response,
            reverse(
                'jobs:all_jobs',
                args=(math.ceil(self.job_count/PAGINATION_AMOUNT),)))

    def test_all_page_context(self):
        self.response = self.client.get(reverse('jobs:all_jobs', args=(1,)))
        self.assertIsInstance(self.response.context['jobs'], Page)


class SpecificJobPageTest(TestCase):

    def setUp(self):
        self.job = DummyJobManager().create_and_save_job()
        self.response = self.client.get(reverse(
            'jobs:specific_job',
            args=(self.job.id,)))

    def test_specific_job_page_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'jobs/specific_job.html')

    def test_specific_job_page_has_corresponding_title_to_job(self):
        self.assertContains(
            self.response,
            '<title>{0} | Diákmunka most!</title>'.format(self.job.title))

    def test_specific_job_page_uses_job_context(self):
        self.assertIsInstance(self.response.context['job'], Job)

    def test_specific_job_page_response_code_is_okay(self):
        self.assertEqual(self.response.status_code, 200)

    def test_specific_job_page_displays_title_as_heading(self):
        self.assertContains(
            self.response,
            '<h1 id="job-title">{0}</h1>'.format(self.job.title))

    def test_specific_job_page_displays_job_type(self):
        self.assertContains(
            self.response,
            '<h3 id="job-type">Munka típusa: {0}</h3>'.format(
                self.job.get_job_type_display()))

    def test_specific_job_page_displays_task(self):
        #  ez eleg luzernek tunik, valami jobb megoldas TODO
        self.assertContains(
            self.response,
            '<h3>Feladat leírása:</h3>')
        self.assertContains(
            self.response,
            '<p id="job-task">{0}</p>'.format(self.job.task))

    def test_specific_job_page_displays_place_of_work(self):
        self.assertContains(
            self.response,
            '<h3 id="job-place-of-work">Munkavégzés helye: {0}</h3>'.format(
                self.job.place_of_work))

    def test_specific_job_page_displays_one_salary_if_min_and_max_is_equal_and_not_zero(self):
        self.assertContains(
            self.response,
            '<h3 id="job-salary">Bérezés: {0} Ft/óra</h3>'.format(
                self.job.min_salary))

    #  Ezt a ket tesztet majd refaktor TODO
    def test_specific_job_page_displays_multiple_salaries(self):
        self.job.min_salary = self.job.max_salary - 1
        self.job.save()
        self.response = self.client.get(reverse(
            'jobs:specific_job',
            args=(self.job.id,)))
        self.assertContains(
            self.response,
            '<h3 id="job-salary">Bérezés: {0} - {1} Ft/óra</h3>'.format(
                self.job.min_salary,
                self.job.max_salary))

    def test_specific_job_page_displays_message_if_salary_is_zero(self):
        self.job.min_salary = 0
        self.job.max_salary = 0
        self.job.save()
        self.response = self.client.get(reverse(
            'jobs:specific_job',
            args=(self.job.id,)))
        self.assertContains(
            self.response,
            '<h3 id="job-salary">Bérezés: {0}</h3>'.format(
                Job.UNDEFINED_SALARY_TEXT
            ))

    def test_specific_job_page_displays_working_hours(self):
        self.assertContains(
            self.response,
            '<h3 id="job-working-hours">Munkaidő: {0}</h3>'.format(
                self.job.working_hours))

    def test_specific_job_page_displays_requirements(self):
        self.assertContains(
            self.response,
            '<h3>Feltételek:</h3>')
        self.assertContains(
            self.response,
            '<p id="job-requirements">{0}</p>'.format(self.job.requirements))

    def test_specific_job_page_displays_url_to_actual_job(self):
        element = '<a type="button" id="job-url" class="btn btn-primary btn-lg" href="{0}">Jelentkezem!</a>'
        self.assertContains(self.response, element.format(self.job.url))

    def test_specific_job_page_doesnt_displays_other_info_if_it_empty(self):
        self.assertNotContains(
            self.response,
            '<h3>Egyéb információ:</h3>')
        self.assertNotContains(
            self.response,
            '<p id="job-other-info">{0}</p>'.format(self.job.other_info))

    def test_specific_job_page_displays_other_info_if_it_is_not_empty(self):
        self.job.other_info = "BLABLABLA"
        self.job.save()
        self.response = self.client.get(reverse(
            'jobs:specific_job',
            args=(self.job.id,)))
        self.assertContains(
            self.response,
            '<h3>Egyéb információ:</h3>')
        self.assertContains(
            self.response,
            '<p id="job-other-info">{0}</p>'.format(self.job.other_info))


class SpecificJobPage404Test(TestCase):

    def setUp(self):
        #  eleg csunya, hogy bele van egetve egy szam TODO
        self.NOT_VALID_ID = 123456
        self.response = self.client.get(reverse(
            'jobs:specific_job',
            args=(self.NOT_VALID_ID,)
        ))

    def test_non_existent_job_page_returns_404(self):
        self.assertEqual(self.response.status_code, 404)

    # itt meg a CUSTOM 404 page-t is tesztelni kell pl: title TODO
