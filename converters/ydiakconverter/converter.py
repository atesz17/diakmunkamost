from converters.abstractconverter.converter import AbstractConverter
from converters.exceptions import ConverterException

from jobs.models import Job

import json


class YDiakConverter(AbstractConverter):

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
        raw_salary = raw_salary.replace(" ", "")
        raw_salary = raw_salary.replace("Ft", "")
        min_max_salary = raw_salary.split("/")[0]
        salary_list = min_max_salary.split("-")
        if len(salary_list) == 1:
            return salary_list[0], salary_list[0]
        elif len(salary_list) == 2:
            return salary_list[0], salary_list[1]
        else:
            raise ConverterException(
                "Nem sikerult parsolni a salary-t"
            )
