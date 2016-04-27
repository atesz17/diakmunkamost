from scrapers.abstractscraper.abstractscraper import  AbstractScraper
from scrapers.exceptions import ScraperException
from helpers.methods import get_dynamic_parent_folder
from scrapers.helpers.methods import can_fetch_url, is_job_already_scraped
from scrapers.models import URL, Provider, State

import filecmp
import json
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
        eu = self.__class__
        self.logger.info("Starting euDiakok scraping...")
        if not can_fetch_url(eu.robots, eu.base_url):
            self.logger.error("Cannot fetch url beacuse of robots.txt.")
            return
        if not self.cache_outdated():
            self.logger.info("Cache is up-to-date, not scraping.")
            return
        for html, url in eu.get_jobs():
            self.logger.info("Scraping {}".format(url))
            try:
                job = self.scrape_page(html)
                job["url"] = url
                eu.save(job)
            except ScraperException:
                self.logger.error("Nem sikerult parsolni: {}".format(url))
                continue

    @staticmethod
    def save(job):
        url_obj = URL()
        url_obj.url = job['url']
        del job['url']
        url_obj.state = State.objects.get_or_create(state="scraped")[0]
        url_obj.provider = Provider.objects.get_or_create(
            name = "eudiakok"
        )[0]
        url_obj.scraped_data = json.dumps(job, ensure_ascii=False)
        url_obj.save()

    def scrape_page(self, html):
        soup = BeautifulSoup(html, "html.parser")
        attrs = dict()
        attrs["title"] = soup.find("h2", class_="cimsav").text
        for heading in soup.find_all("h5"):
            if "Munka típusa" in heading.text:
                attrs["job_type"] = heading.find_next("p").text
            elif "Munkavégzés helye" in heading.text:
                place = heading.find_next("p").text
                if "pest" not in place.lower():
                    raise ScraperException
                attrs["place_of_work"] = place
            elif "Feladat" in heading.text:
                attrs["task"] = heading.find_next("p").text
            elif "Fizetés" in heading.text:
                attrs["salary"] = heading.find_next("p").text
            elif "Munkaidő" in heading.text:
                attrs["working_hours"] = heading.find_next("p").text
            elif "Elvárás" in heading.text:
                attrs["requirements"] = heading.find_next("p").text
            elif "Egyéb" in heading.text:
                attrs["other"] = heading.find_next("p").text
        return attrs


    @staticmethod
    def get_jobs():
        eu = EuDiakokScraper
        for url in eu.get_job_links():
            if not is_job_already_scraped(url):
                yield requests.get(url).text, url

    @staticmethod
    def get_job_links():
        eu = EuDiakokScraper
        html = requests.get(eu.base_url).text
        soup = BeautifulSoup(html, "html.parser").find(
            "div", id="munkakListaContainer")
        for munkabox in soup.find_all("div", class_="munkabox"):
            yield munkabox.find("a")["href"]

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

