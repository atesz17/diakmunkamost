from converters import AbstractConverter

from jobs.models import Job

import json


class YDiakConverter(AbstractConverter):

    def convert_job_type(self, scraped_job):
        super_ret = super(YDiakConverter, self).convert_job_type(scraped_job)
        if super_ret == "Egyéb":
            raw_job_type = json.loads(scraped_job.scraped_data['job_type'])
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
