from django.apps import AppConfig

from converters.ydiakconverter.ydiakconverter import YDiakConverter
from converters.eudiakokconverter.eudiakokconverter import EuDiakokConverter
from converters.schonherzconverter.schnoherzconverter import SchonherzConverter

class ConvertersConfig(AppConfig):
    name = 'converters'
    converter_classes = [
        ("ydiak", YDiakConverter),
        ("eudiakok", EuDiakokConverter),
        ("schonherz", SchonherzConverter)
    ]
