from django.core.management.base import BaseCommand, CommandError

from converters.apps import ConvertersConfig
from converters.abstractconverter.abstractconverter import AbstractConverter


class Command(BaseCommand):
    help = 'Starts converting the specified scraped job'

    def handle(self, *args, **options):
        for converter_class in ConvertersConfig.converter_classes:
            converter = converter_class()
            if isinstance(converter, AbstractConverter):
                converter.convert()