from converters.abstractconverter.abstractconverter import AbstractConverter
from converters.exceptions import ConverterException

from helpers.methods import replace_with_empty_char, are_substrings_in_string
from jobs.models import Job

import json


class SchonherzConverter(AbstractConverter):

    to_be_replaced_words = {
        "salary": ["Br.", "Ft/óra", "Ft/ óra", " ", r"\r", r"\n"]
    }
    job_types_synonyms = {
        "informatikai": ["fejleszto", "informatikus", "szoftvertesztelo",
                         "sitebuilder", "mobil-fejlesztes", "otthonrol-vegezheto",
                         "support"],
        "irodai" : ["adminisztrativ"],
        "fizikai" : ["fizikai"],
        "hostess" : ["hostess", "betanitott"],
        "muszaki" : ["gepeszmernok", "egyeb-muszaki"]
    }

    def convert_job_type(self, scraped_job):
        sh = SchonherzConverter
        super_ret = super(SchonherzConverter, self).convert_job_type(scraped_job)
        if super_ret == "Egyéb":
            raw_job_type = json.loads(scraped_job.scraped_data)['job_type']
            for key, value in sh.job_types_synonyms.items():
                if are_substrings_in_string(raw_job_type.lower(), value):
                    return Job.PREDEFINED_JOB_TYPES[key]
        return super_ret

    def convert_salary(self, scraped_job):
        sh = SchonherzConverter
        raw_salary = json.loads(scraped_job.scraped_data)['salary']
        raw_salary = replace_with_empty_char(
            raw_salary,
            sh.to_be_replaced_words['salary']
        )
        salary_list = raw_salary.split("-")
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