from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts converting the specified scraped job'

    def handle(self, *args, **options):
        pass