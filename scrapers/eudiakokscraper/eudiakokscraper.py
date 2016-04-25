from scrapers.abstractscraper.abstractscraper import  AbstractScraper
from scrapers.exceptions import ScraperException
from helpers.methods import get_dynamic_parent_folder
from scrapers.helpers.methods import can_fetch_url

import os
from urllib.robotparser import RobotFileParser

from bs4 import BeautifulSoup


class EuDiakokScraper:

    base_url = "http://www.eudiakok.hu/diakmunka/megye/budapest"
    robots = "http://www.eudiakok.hu/robots.txt"
    cache = ".cache.html"

    def __init__(self, cache_file_name=".cache.html"):
        self.cache = os.path.join(
            get_dynamic_parent_folder(self.__class__),
            cache_file_name)

    @staticmethod
    def scrape():
        eu = EuDiakokScraper
        if can_fetch_url(eu.robots, eu.base_url):
            pass

    @staticmethod
    def update_cache(new_data):
        with open(EuDiakokScraper.cache) as cache_file:
            cache_file.write(new_data)


