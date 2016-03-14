from django.apps import AppConfig

from scrapers.ydiakscraper.ydiakscraper import YDiakScraper


class ScrapersConfig(AppConfig):
    name = 'scrapers'
    scraper_classes = [
        YDiakScraper,
    ]
