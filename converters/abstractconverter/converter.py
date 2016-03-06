from abc import ABCMeta, abstractmethod
import configparser
import os
import inspect


class AbstractConverter(metaclass=ABCMeta):
    """
    Abstract osztaly, ez mindegyik Converter osztalynak az alapja
    """

    def __init__(self, config_file_name="converter.ini"):
        config_file = os.path.join(self.get_parent_folder(), config_file_name)
        config = configparser.ConfigParser()
        config.read(config_file)
        self.__read_configuration(config)

    def get_parent_folder(self):
        return os.path.dirname(inspect.getfile(self.__class__))

    def __read_configuration(self, config):
        config = config['DEFAULT']
        self.provider_name = config['ProviderName']

    @abstractmethod
    def convert(self):
        """
        Lekerdezi a tablakbol a <provider_name> scrapelt munkakat, es megprobalja
        convertalni oket. Ha esetleg hiba volt a convertalas soran, a fuggveny
        visszaad egy dictionary-t a hibakkal egyutt, illetve a db-be is beleirja
        hogy a statusza az adott munkanak converter_error
        :return:
        """
        pass