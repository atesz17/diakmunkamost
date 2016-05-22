from django.apps import AppConfig

from scrapers.ydiakscraper.ydiakscraper import YDiakScraper
from scrapers.eudiakokscraper.eudiakokscraper import EuDiakokScraper
from scrapers.schonherzscraper.schonherzscraper import SchonherzScraper


class ScrapersConfig(AppConfig):
    """
    Ez az osztaly tarol referenciakat a scraper osztalyokra.
    """
    name = 'scrapers'
    scraper_classes = [
        ("ydiak", YDiakScraper),
        ("eudiakok", EuDiakokScraper),
        ("schonherz", SchonherzScraper)
    ]
