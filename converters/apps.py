from django.apps import AppConfig

from converters.ydiakconverter.converter import YDiakConverter

class ConvertersConfig(AppConfig):
    name = 'converters'
    converter_classes = [
        YDiakConverter,
    ]
