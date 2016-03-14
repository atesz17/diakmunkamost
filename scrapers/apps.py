from django.apps import AppConfig

from scrapers.ydiakscraper.ydiakscraper import YDiakScraper


class ScrapersConfig(AppConfig):
    """
    Ez az osztaly tarol referenciakat a scraper osztalyokra.
    """
    name = 'scrapers'
    scraper_classes = [
        YDiakScraper,
    ]
