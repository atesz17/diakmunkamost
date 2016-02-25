from django.apps import AppConfig

from scrapers.ydiakscraper.scraper import YDiakScraper


class ScrapersConfig(AppConfig):
    name = 'scrapers'
    scraper_classes = [
        YDiakScraper,
    ]
