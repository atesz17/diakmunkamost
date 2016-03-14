from django.apps import AppConfig

from converters.ydiakconverter.ydiakconverter import YDiakConverter

class ConvertersConfig(AppConfig):
    name = 'converters'
    converter_classes = [
        YDiakConverter,
    ]
