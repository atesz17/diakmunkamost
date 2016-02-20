from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from jobs.models import Job

from .helper import DummyJobManager


class JobModelTest(TestCase):

    def test_cannot_save_empty_job(self):
        job = Job()
        with self.assertRaises(IntegrityError):
            job.save()

    def test_cannot_save_job_which_min_salary_is_greater_than_max_salary(self):
        job = DummyJobManager().create_job()
        job.max_salary = job.min_salary - 1
        with self.assertRaises(ValidationError):
            job.full_clean()
            job.save()

    def test_can_save_job_where_min_salary_equals_max_salary(self):
        job = DummyJobManager().create_job()
        self.assertEqual(0, Job.objects.all().count())
        job.save()
        self.assertEqual(1, Job.objects.all().count())

    def test_job_object_can_be_saved_leaving_other_info_field_empty(self):
        job = DummyJobManager().create_job()
        job.other_info = ''
        self.assertEqual(0, Job.objects.all().count())
        job.save()
        self.assertEqual(1, Job.objects.all().count())

    def test_saved_object_can_be_retrieved(self):
        job = DummyJobManager().create_and_save_job()
        self.assertEqual(job, Job.objects.get(id=job.id))
