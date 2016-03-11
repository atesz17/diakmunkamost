from abc import ABCMeta
import configparser
import os
import inspect
import json

from jobs.models import Job
from scrapers.models import URL

class AbstractConverter(metaclass=ABCMeta):
    """
    Abstract osztaly, ez mindegyik Converter osztalynak az alapja
    """

    def __init__(self):
        self.title = None
        self.job_type = None
        self.provider_name = None

    def __init__(self, config_file_name="converter.ini"):
        config_file = os.path.join(self.get_parent_folder(), config_file_name)
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
        for scraped_job in URL.objects.filter(
                provider__name=self.provider_name):
            self.title = self.convert_title(scraped_job)
            self.job_type = self.convert_job_type(scraped_job)
            # es majd db insert legutolso lepeskent

    def convert_title(self, scraped_job):
        raw_title = json.loads(scraped_job.scraped_data)['title']
        return raw_title

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