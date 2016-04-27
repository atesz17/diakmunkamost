from converters.abstractconverter.abstractconverter import AbstractConverter
from converters.exceptions import ConverterException

import json


class EuDiakokConverter(AbstractConverter):

    def convert_salary(self, scraped_job):
        raw_salary = json.loads(scraped_job.scraped_data)["salary"]
        ints_int_raw_salary = []
        for part in raw_salary.split(" "):
            try:
                ints_int_raw_salary.append(int(part))
            except ValueError:
                # this part is NaN
                pass
        if len(ints_int_raw_salary) == 2:
            if ints_int_raw_salary[0] <= ints_int_raw_salary[1]:
                return ints_int_raw_salary
            raise ConverterException("Unable to parse salary")
        elif len(ints_int_raw_salary) == 1:
            return ints_int_raw_salary * 2
        else:
            raise ConverterException("Unable to parse salary")
