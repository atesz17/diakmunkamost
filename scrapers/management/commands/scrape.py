from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts scraping the specified job page'

    def handle(self, *args, **options):
        scrapers = self.get_scrapers()

    def get_scrapers(self):
        pass
