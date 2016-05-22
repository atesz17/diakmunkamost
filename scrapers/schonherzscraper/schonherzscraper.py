from helpers.methods import get_dynamic_parent_folder
from scrapers.exceptions import ScraperException
from scrapers.models import URL, Provider, State

import os
import json
import logging
import filecmp
import urllib.parse

import requests
from bs4 import BeautifulSoup


class SchonherzScraper:

    budapest_jobs = "https://schonherz.hu/hirdetesek/Budapest"
    base_url = "https://schonherz.hu"
    target_categories = ["fejleszto", "adminisztrativ", "support",
                         "hostess", "informatikus", "betanitott",
                         "szoftvertesztelo", "sitebuilder", "egyeb-muszaki",
                         "mobil-fejlesztes", "otthonrol-vegezheto"]

    def __init__(self, cache_file_name=".cache.html"):
        self.cache = os.path.join(
            get_dynamic_parent_folder(self.__class__),
            cache_file_name)

    @property
    def logger(self):
        name = '.'.join(["scrapers", self.__class__.__name__])
        return logging.getLogger(name)

    def scrape(self, force):
        """
        Scrapes the site. Doesn't check robots.txt, because the site doesn't
        provide one.
        """
        sh = self.__class__
        self.logger.info("Starting schonherz scraping...")
        if force or not self.cache_outdated():
            self.logger.info("Cache is up-to-date, not scraping")
            return
        for category_url in sh.get_categories():
            if category_url.split("/")[-1] in sh.target_categories:
                category_name = category_url.split("/")[-1]
                for html, url in sh.get_jobs(category_url):
                    self.logger.info("Scraping {}".format(url))
                    try:
                        job = sh.scrape_page(html)
                        job["url"] = url
                        job["job_type"] = category_name
                        sh.save(job)
                    except ScraperException:
                        self.logger.error("SCRAPER ERROR: {}".format(url))
                        continue

    @staticmethod
    def save(job):
        url_obj = URL()
        url_obj.url = job['url']
        del job['url']
        url_obj.state = State.objects.get_or_create(state="scraped")[0]
        url_obj.provider = Provider.objects.get_or_create(
            name="schonherz"
        )[0]
        url_obj.scraped_data = json.dumps(job, ensure_ascii=False)
        url_obj.save()

    @staticmethod
    def get_jobs(category_url):
        sh = SchonherzScraper
        html = requests.get(category_url).text
        soup = BeautifulSoup(html, "html.parser").find("div", class_="list")
        # 2 different div classes
        jobs = []
        jobs.append(soup.find_all("div", "projectad-list-item"))
        jobs.append(soup.find_all("div", "projectad-list-item alternate"))
        for job in jobs:
            job_soup = BeautifulSoup(job, "html.parser").find()


    @staticmethod
    def get_categories():
        """
        Returns urls pointing to different categories on the site

        :return: iterable urls
        """
        sh = SchonherzScraper
        html = requests.get(sh.budapest_jobs).text
        soup = BeautifulSoup(html, "html.parser").find(
            "div", class_="categories")
        for rel_link in soup.find_all("a")["href"]:
            yield urllib.parse.urljoin(sh.base_url, rel_link)

    def cache_outdated(self):
        """
        Downloads and compares the current state of the job board, and
        compares it to the cache.

        :return: True, if cache is outdated
        """
        sh = self.__class__
        html = requests.get(sh.budapest_jobs).text
        soup = BeautifulSoup(html, 'html.parser')
        jobs = soup.find("div", class_="categories")
        current = os.path.join(
            get_dynamic_parent_folder(sh),
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

    def update_cache(self, new_data):
        with open(self.cache, "w") as cache_file:
            cache_file.write(new_data)