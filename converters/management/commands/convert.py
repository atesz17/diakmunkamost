from django.core.management.base import BaseCommand, CommandError

from converters.apps import ConvertersConfig
from converters.abstractconverter.abstractconverter import AbstractConverter


class Command(BaseCommand):
    help = 'Starts converting the specified scraped job'

    def add_arguments(self, parser):
        parser.add_argument("converters", nargs="*")

    def handle(self, *args, **options):
        for converter_name, converter_klass in ConvertersConfig.converter_classes:
            if len(options["converters"]) == 0:  # no specific conv were given
                converter_klass().convert()
            else:
                if converter_name in options["converters"]:
                    converter_klass().convert()