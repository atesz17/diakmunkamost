from scrapers.abstractscraper.abstractscraper import  AbstractScraper
from scrapers.exceptions import ScraperException
from helpers.methods import get_dynamic_parent_folder
from scrapers.helpers.methods import can_fetch_url

import filecmp
import os
import logging

from bs4 import BeautifulSoup
import requests


class EuDiakokScraper:

    base_url = "http://www.eudiakok.hu/diakmunka/megye/budapest"
    robots = "http://www.eudiakok.hu/robots.txt"

    def __init__(self, cache_file_name=".cache.html"):
        self.cache = os.path.join(
            get_dynamic_parent_folder(self.__class__),
            cache_file_name)

    @property
    def logger(self):
        name = '.'.join(["scrapers", self.__class__.__name__])
        return logging.getLogger(name)

    def scrape(self):
        eu = EuDiakokScraper
        self.logger.info("Starting euDiakok scraping...")
        if not can_fetch_url(eu.robots, eu.base_url):
            self.logger.error("Cannot fetch url beacuse of robots.txt.")
            return
        if not self.cache_outdated():
            self.logger.info("Cache is up-to-date, not scraping.")
            return

    def update_cache(self, new_data):
        with open(self.cache, "w") as cache_file:
            cache_file.write(new_data)

    def cache_outdated(self):
        """
        Downloads and compares the current state of the job board, and
        compares it to the cache.

        :return: True, if cache is outdated
        """
        eu = EuDiakokScraper
        html = requests.get(eu.base_url).text
        soup = BeautifulSoup(html, 'html.parser')
        jobs = soup.find("div", id="munkakListaContainer")
        current = os.path.join(
            get_dynamic_parent_folder(EuDiakokScraper),
            ".current.html")
        with open(current, "w") as f:
            f.write(str(jobs))
        cache_outdated = True
        if os.path.isfile(self.cache):
            if filecmp.cmp(current, self.cache):
                cache_outdated = False
        else:
            self.update_cache(str(jobs))
        os.remove(current)
        return cache_outdated

