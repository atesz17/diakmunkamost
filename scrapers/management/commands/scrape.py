from django.core.management.base import BaseCommand, CommandError

from scrapers.apps import ScrapersConfig


class Command(BaseCommand):
    help = 'Starts scraping the specified job page'

    def add_arguments(self, parser):
        parser.add_argument("scrapers", nargs="*")

    def handle(self, *args, **options):
        """

        CODE SMELL: 2x scraper_klass

        :param args:
        :param options: arguments given from command
        """
        for scraper_name, scraper_klass in ScrapersConfig.scraper_classes:
            if len(options["scrapers"]) == 0: # no specific scrapers were given
                scraper_klass().scrape()
            else:
                if scraper_name in options["scrapers"]:
                    scraper_klass().scrape()





