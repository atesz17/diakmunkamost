from converters import AbstractConverter

from scrapers.models import URL


class YDiakConverter(AbstractConverter):

    def convert(self):
        """
        Lekerdezi a tablakbol az ydiak scrapelt munkakat, es megprobalja
        convertalni oket. Ha esetleg hiba volt a convertalas soran, a fuggveny
        visszaad egy dictionary-t a hibakkal egyutt, illetve a db-be is beleirja
        hogy a statusza az adott munkanak converter_error
        :return:
        """
        for scraped_job in URL.objects.filter(provider_name=self.provider_name):
            pass # Itt jon maga a mezonkenti scrapeles