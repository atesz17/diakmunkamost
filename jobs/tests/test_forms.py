from django.test import TestCase

from jobs.forms import AllJobSearchForm
from jobs.models import Job


class AllJobSearchFormTest(TestCase):

    def test_form_has_correct_job_choices(self):
        form = AllJobSearchForm()
        self.assertEqual(Job.JOB_TYPES, form.fields['job_types'].choices)

    def test_form_has_correct_labels(self):
        form = AllJobSearchForm()
        self.assertEqual('Munka típusa', form.fields['job_types'].label)
        self.assertEqual(
            'Minumum órabér (Ft/óra)',
            form.fields['min_salary'].label)
