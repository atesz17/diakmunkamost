from django.core.management.base import BaseCommand, CommandError

from scrapers.apps import ScrapersConfig

import importlib

class Command(BaseCommand):
    help = 'Starts scraping the specified job page'

    def handle(self, *args, **options):
        """
        A szep megoldas az lenne, ahogy django source-ban is van ld:
        execute_from_command_line hogy mukodik
        ugy lenne szep, hogy mindegyik scraper package-tol megkoveteljuk
        hogy a scraper neveben szerepeljen a 'scraper' szo (mint a testnel)
        es automatikusan megtalalja azokat a packageket/modulokat,
        beimportalja es vegrehajtja oket. Most egyelore az apps.py-ban
        meg kell adni a scraper package-k nevet
        """
        for package_name in ScrapersConfig.scrapers:
            scraper_module = ''
            try:
                scraper_module = importlib.import_module(
                    "scrapers.{0}.scraper".format(package_name)
                )
            except ImportError:
                print('No package name was found by the name: {0}, '
                      'check scrapers/apps.py'.format(package_name))
                continue




