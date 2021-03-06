from helpers.methods import get_dynamic_parent_folder
from scrapers.exceptions import ScraperException
from scrapers.models import URL, Provider, State

import os
import json
import logging
import filecmp
import urllib.parse
import re

import requests
from bs4 import BeautifulSoup


def nvltext(element):
    """
    Accepts any beautifulsoup element, if it's None, then the function
    returns empty string

    :param element:
    :return:
    """
    if element is None:
        return ""
    return element.text


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
                        except (ScraperException, AttributeError):
                            self.logger.error("SCRAPER ERROR: {}".format(url))
                            continue
        else:
            self.logger.info("Cache is up-to-date, not scraping")
            return

    @staticmethod
    def scrape_page(html):
        """
        worst page structure ever #killme

        :param html:
        :return:
        """
        attrs = dict()
        attrs["title"] = BeautifulSoup(html, "html.parser").find(
            "div",
            id="projectad-details").find(
                "div",
                class_="title").text

        soup = BeautifulSoup(html, "html.parser")
        attrs["task"] = "Honlapon bővebb információ" #  erre valahogy szurni kene
        attrs["place_of_work"] = str(
            soup.find("p", text=re.compile(r"Munkavégzés helye")).next_sibling)
        attrs["salary"] = str(
            soup.find("p", text=re.compile(r"Fizetés")).next_sibling)
        attrs["working_hours"] = str(
            soup.find("p", text=re.compile(r"Minimum heti óraszám")).next_sibling)
        attrs["requirements"] = str(
            soup.find("p", text=re.compile(r"Elvárások")).next_sibling)
        return attrs



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
        for job in soup.find_all("div", class_="projectad-list-item"):
            post_url = job.find("a")["href"]
            full_url = urllib.parse.urljoin(sh.base_url, post_url)
            yield requests.get(full_url).text, full_url


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
        for rel_link in soup.find_all("a"):
            full_url = urllib.parse.urljoin(sh.base_url, rel_link["href"])
            yield full_url

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