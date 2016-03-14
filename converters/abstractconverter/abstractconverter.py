from abc import ABCMeta, abstractmethod
import configparser
import os
import inspect
import json

from converters.exceptions import ConverterException
from helpers.methods import get_dynamic_parent_folder
from jobs.models import Job, JobProvider, JobType
from jobs.forms import JobForm
from scrapers.models import URL, State


class AbstractConverter(metaclass=ABCMeta):
    """
    Abstract osztaly, ez mindegyik Converter osztalynak az alapja
    """

    def __init__(self, config_file_name="converter.ini"):
        self.title = None
        self.job_type = None
        self.task = None
        self.place_of_work = None
        self.min_salary = None
        self.max_salary = None
        self.requirements = None
        self.working_hours = None
        self.other = None
        self.url = None
        config_file = os.path.join(
            get_dynamic_parent_folder(self.__class__),
            config_file_name)
        config = configparser.ConfigParser()
        config.read(config_file)
        self.__read_configuration(config)

    def get_parent_folder(self):
        return os.path.dirname(inspect.getfile(self.__class__))

    def __read_configuration(self, config):
        config = config['DEFAULT']
        self.provider_name = config['ProviderName']

    def convert(self):
        """
        Lekerdezi a tablakbol a <provider_name> scrapelt munkakat, es megprobalja
        convertalni oket. Ha esetleg hiba volt a convertalas soran, a fuggveny
        visszaad egy dictionary-t a hibakkal egyutt, illetve a db-be is beleirja
        hogy a statusza az adott munkanak converter_error
        :return:
        """
        scraped_jobs = URL.objects.filter(
            provider__name=self.provider_name
        ).filter(
            state__state="scraped"
        )
        for scraped_job in scraped_jobs:
            self.title = self.convert_title(scraped_job)
            self.job_type = self.convert_job_type(scraped_job)
            self.task = self.convert_task(scraped_job)
            #  csak pesti munka, nem is ellenorizzuk a valodi erteket
            self.place_of_work = "Pest"
            #  es majd db insert legutolso lepeskent
            try:
                self.min_salary, self.max_salary = self.convert_salary(
                    scraped_job
                )
            except ConverterException:
                scraped_job.state = State.objects.get_or_create(
                    state="converter_error"
                )[0]
                scraped_job.save()
                print("Converter error (salary)")
                continue
            self.requirements = self.convert_requirements(scraped_job)
            self.working_hours = self.convert_working_hours(scraped_job)
            self.other = self.convert_other(scraped_job)
            self.url = scraped_job.url
            self.save_job()
            scraped_job.state = State.objects.get_or_create(
                state="converted"
            )[0]
            scraped_job.save()

    def convert_title(self, scraped_job):
        return json.loads(scraped_job.scraped_data)['title']

    def convert_job_type(self, scraped_job):
        raw_job_type = json.loads(scraped_job.scraped_data)['job_type']
        if "fizikai" in raw_job_type.lower():
            return Job.PREDEFINED_JOB_TYPES['fizikai']
        elif "irodai" in raw_job_type.lower():
            return Job.PREDEFINED_JOB_TYPES['irodai']
        elif "telefonos" in raw_job_type.lower():
            return Job.PREDEFINED_JOB_TYPES['telefonos']
        elif "hostess" in raw_job_type.lower():
            return Job.PREDEFINED_JOB_TYPES['hostess']
        elif "műszaki" in raw_job_type.lower():
            return Job.PREDEFINED_JOB_TYPES['muszaki']
        elif "informatikai" in raw_job_type.lower():
            return Job.PREDEFINED_JOB_TYPES['informatikai']
        elif "áruházi" in raw_job_type.lower():
            return Job.PREDEFINED_JOB_TYPES['aruhazi/vendeglatos']
        elif "vendéglátos" in raw_job_type.lower():
            return Job.PREDEFINED_JOB_TYPES['aruhazi/vendeglatos']
        return Job.PREDEFINED_JOB_TYPES['egyeb']

    def convert_task(self, scraped_job):
        return json.loads(scraped_job.scraped_data)['task']

    @abstractmethod
    def convert_salary(self, scraped_job):
        pass

    def convert_requirements(self, scraped_job):
        return json.loads(scraped_job.scraped_data)['requirements']

    def convert_working_hours(self, scraped_job):
        return json.loads(scraped_job.scraped_data)['working_hours']

    def convert_other(self, scraped_job):
        return json.loads(scraped_job.scraped_data)['other']

    def save_job(self):
        form = JobForm({
            "title": self.title,
            "task": self.task,
            "place_of_work": self.place_of_work,
            "min_salary": self.min_salary,
            "max_salary": self.max_salary,
            "requirements": self.requirements,
            "working_hours": self.working_hours,
            "other": self.other,
            "url": self.url,
            }
        )
        # itt megtortenik a validation is, mert meg nem volt is_valid() hivas
        job = form.save(commit=False)
        job.job_type = JobType.objects.get_or_create(name = self.job_type)[0]
        job.job_provider = JobProvider.objects.get_or_create(
                name = self.provider_name
        )[0]
        job.save()

