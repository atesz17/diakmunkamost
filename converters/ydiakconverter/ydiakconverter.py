from converters.abstractconverter.abstractconverter import AbstractConverter
from converters.exceptions import ConverterException

from helpers.methods import replace_with_empty_char, are_substrings_in_string
from jobs.models import Job

import json


class YDiakConverter(AbstractConverter):

    def __init__(self, config_file_name="converter.ini"):
        super(YDiakConverter, self).__init__(config_file_name)
        self.to_be_replaced_words = {
            'salary': [" ", "Ft", "Forint"]
        }
        self.job_types_synonyms = {
            'aruhazi/vendeglatos': ["bolti", "pénztáros"],
            'irodai': ['ibm']
        }



    def convert_job_type(self, scraped_job):
        super_ret = super(YDiakConverter, self).convert_job_type(scraped_job)
        if super_ret == "Egyéb":
            raw_job_type = json.loads(scraped_job.scraped_data)['job_type']
            for key, value in self.job_types_synonyms.items():
                if are_substrings_in_string(raw_job_type.lower(), value):
                    return Job.PREDEFINED_JOB_TYPES[key]
        return super_ret

    def convert_salary(self, scraped_job):
        raw_salary = json.loads(scraped_job.scraped_data)['salary']
        raw_salary = replace_with_empty_char(
            raw_salary,
            self.to_be_replaced_words['salary']
        )
        min_max_salary = raw_salary.split("/")[0]
        salary_list = min_max_salary.split("-")
        try:
            if len(salary_list) == 1:
                return int(salary_list[0]), int(salary_list[0])
            elif len(salary_list) == 2:
                return int(salary_list[0]), int(salary_list[1])
            else:
                raise ConverterException()
        except (ValueError, ConverterException):
            #  Ezt azert valahogy jobban illene majd lekezelni
            return 0, 0
