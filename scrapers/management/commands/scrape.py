from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts scraping the specified job page'

    def handle(self, *args, **options):
        scrapers = self.get_scrapers()
        '''
        for scraper in options['scrape']:
            if scraper == "ydiak":
                YDiakScraper().scrape
            else:
                raise CommandError("{0} named scraper doesnt exist")
        '''

    def get_scrapers(self):
        pass
