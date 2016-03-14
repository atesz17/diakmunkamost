from converters.abstractconverter.abstractconverter import AbstractConverter
from converters.exceptions import ConverterException

from helpers.methods import replace_with_empty_char
from jobs.models import Job

import json


class YDiakConverter(AbstractConverter):

    def __init__(self, config_file_name="converter.ini"):
        super(YDiakConverter, self).__init__(config_file_name)
        self.to_be_replaced_words = {
            'salary': [" ", "Ft", "Forint"]
        }
        self.accepted_strings = {
            'job_type': ["bolti", "pénztáros", "ibm"]
        }

    def convert_job_type(self, scraped_job):
        super_ret = super(YDiakConverter, self).convert_job_type(scraped_job)
        if super_ret == "Egyéb":
            raw_job_type = json.loads(scraped_job.scraped_data)['job_type']
            if "bolti" in raw_job_type.lower():
                return Job.PREDEFINED_JOB_TYPES['aruhazi/vendeglatos']
            if "pénztáros" in raw_job_type.lower():
                return Job.PREDEFINED_JOB_TYPES['aruhazi/vendeglatos']
            """
            Nagyon sok IBM-s munka van az YDiakon (10+), nem informatikai
            jelleguek, inkabb irodaiak
            """
            if "ibm" in raw_job_type.lower():
                return Job.PREDEFINED_JOB_TYPES['irodai']
        return super_ret

    def convert_salary(self, scraped_job):
        raw_salary = json.loads(scraped_job.scraped_data)['salary']
        raw_salary = replace_with_empty_char(
            raw_salary,
            self.to_be_replaced_words['salary']
        )
        min_max_salary = raw_salary.split("/")[0]
        salary_list = min_max_salary.split("-")
        if len(salary_list) == 1:
            try:
                return int(salary_list[0]), int(salary_list[0])
            except ValueError:
                raise ConverterException("Nem integer a salary")
        elif len(salary_list) == 2:
            try:
                return int(salary_list[0]), int(salary_list[1])
            except ValueError:
                raise ConverterException("Nem integer a salary")
        else:
            raise ConverterException(
                "Nem sikerult parsolni a salary-t"
            )
