from django.apps import AppConfig

from converters.ydiakconverter.ydiakconverter import YDiakConverter
from converters.eudiakokconverter.eudiakokconverter import EuDiakokConverter

class ConvertersConfig(AppConfig):
    name = 'converters'
    converter_classes = [
        ("ydiak", YDiakConverter),
        ("eudiakok", EuDiakokConverter)
    ]
