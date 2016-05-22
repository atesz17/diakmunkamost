from django.core.management.base import BaseCommand, CommandError

from scrapers.apps import ScrapersConfig


class Command(BaseCommand):
    help = 'Starts scraping the specified job page'

    def add_arguments(self, parser):
        parser.add_argument("scrapers", nargs="*")
        parser.add_argument("--force",
                            help="scrapes the website from scratch, ignores"
                                 "whether there is a valid cache",
                            action="store_true",
                            default=False,
                            dest="force")

    def handle(self, *args, **options):
        """

        CODE SMELL: 2x scraper_klass

        :param args:
        :param options: arguments given from command
        """
        for scraper_name, scraper_klass in ScrapersConfig.scraper_classes:
            if len(options["scrapers"]) == 0: # no specific scrapers were given
                scraper_klass().scrape(options["force"])
            else:
                if scraper_name in options["scrapers"]:
                    scraper_klass().scrape(options["force"])





