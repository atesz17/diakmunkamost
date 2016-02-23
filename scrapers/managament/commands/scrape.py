from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts scraping the specified job page'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("It works!"))
        '''
        for scraper in options['scrape']:
            if scraper == "ydiak":
                YDiakScraper().scrape
            else:
                raise CommandError("{0} named scraper doesnt exist")
        '''
