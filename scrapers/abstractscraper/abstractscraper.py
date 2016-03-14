from abc import ABCMeta, abstractmethod
import configparser
import filecmp
import inspect
import json
import logging
import os
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup

from helpers.methods import get_dynamic_parent_folder
from scrapers.exceptions import ScraperException
from scrapers.models import URL, State, Provider


class BaseScraper(metaclass=ABCMeta):
    """
    Minden scrapernek az abstract ososztalya.
    """

    def __init__(self, config_file_name="scraper.ini"):
        config_file = os.path.join(
            get_dynamic_parent_folder(self.__class__),
            config_file_name)
        config = configparser.ConfigParser()
        config.read(config_file)
        self.__read_configuration(config)

    @property
    def logger(self):
        """
        Nem modul szintu loggolas, hanem osztalyszintut tesz lehetove
        :return: logger objektum
        """
        name = '.'.join([__name__, self.__class__.__name__])
        return logging.getLogger(name)

    def __read_configuration(self, config):
        """
        Azoknal az ertekeknel, ami mindenkeppen specifikus, ott a [] operatort
        kell hasznalni, ahol elkepzelheto deafult value, ott a get()-et
        - name: Tudjuk, hogy melyik oldalt szedjuk le
        - all_job_url: az url cim, ahol az osszes munka listazva van
        - all_job_container_html_tag: ha esetleg az oldal kerete valtozna, de
        maga az osszes munka nem, akkor ne scrapeljunk foloslegesen
        - single_job_html_tag: hogy az oldalon levo munkakon vegig tudjunk
        iteralni
        - cache: eltaroljuk a legutobbi scrapelt oldal html contentet, hogy
        csak akkor szedjuk le uj infot, amikor tenyleg valtozott az oldal
        - json: scrapelt adatok, ezek mennek majd tovabb a converternek
        """
        config = config['DEFAULT']
        self.provider_name = config['ProviderName']
        self.base_url = config['BaseUrl']
        self.all_job_url = config['AllJobUrl']
        self.all_job_container_html_element = \
            config['AllJobContainerHtmlElement']
        self.all_job_container_html_class = config['AllJobContainerHtmlClass']
        self.single_job_html_tag = config['SingleJobHtmlTag']
        self.single_job_href_tag = config['SingleJobHrefTag']
        self.cache = os.path.join(
            get_dynamic_parent_folder(self.__class__),
            config.get('Cache', '.cache.html'))
        self.json = os.path.join(
            get_dynamic_parent_folder(self.__class__),
            config.get('JSON', '.scraped_jobs.json'))
        self.job_attrs = {}

    def scrape(self):
        """
        Ez aja a keretet maganak a scrapeles folyamatanak. Nem ajanlott
        felulirni
        :param force_update: Nem lenyeges, hogy a cache outdatelt vagy nem,
        mindenkeppen frissiteni fogja a jobokat
        :return:
        """
        if not self.is_scraping_allowed():
            """
            azert ezt illene egy kicsit kiboviteni (melyik URL-en, melyik
            szabalynal hasalt el a vizsgalat)
            """
            raise ScraperException("Robots.txt doesn't allow scraping")
        if self.is_cache_outdated():
            for job_html, job_url in self.get_jobs():
                try:
                    self.gather_specific_job_info(job_html)
                except ScraperException as err:
                    print(err)
                    continue # nem pesti munka volt
                self.job_attrs['url'] = job_url
                self.update_scraped_db()
        else:
            self.logger.info(
                "Az oldal tartalma nem valtozott a legutobbi scrapeles ota "
                "(Cache megegyezik az oldallal)"
            )

    def update_scraped_db(self):
        """
        Felvesszuk a job-ot a db-be, es beallituk a statuszat scraped-re
        :param job:
        :return:
        """
        url_obj = URL()
        url_obj.url = self.job_attrs['url']
        url_obj.state = State.objects.get_or_create(state="scraped")[0]
        url_obj.provider = Provider.objects.get_or_create(
            name = self.provider_name
        )[0]
        url_obj.scraped_data = json.dumps(self.job_attrs, ensure_ascii=False)
        url_obj.save()

    def get_jobs(self):
        """
        All job pagen vegigiteralunk az osszes munkan, amiket tovabb adunk a
        gather_specific_job_info() fgv-nek
        :return:
        """
        root_html = requests.get(urljoin(self.base_url, self.all_job_url)).text
        soup = BeautifulSoup(root_html, 'html.parser')
        for job in soup.find_all("a", class_=self.single_job_href_tag):
            if self.is_job_already_scraped(job['href']):
                continue
            yield requests.get(job['href']).text, job['href']

    def is_job_already_scraped(self, job_url):
        try:
            job = URL.objects.get(pk=job_url)
            return True
        except URL.DoesNotExist:
            return False

    def is_scraping_allowed(self):
        """
        Megnezi, hogy a robots.txt nem tiltja-e a scrapelest. Nem igazan teljes
        az ellenorzes, mert csak az all job url-t vizsgalja.
        :return:
        """
        robot_parser = RobotFileParser()
        robots_url = urljoin(self.base_url, 'robots.txt')
        robot_parser.set_url(robots_url)
        robot_parser.read()
        if robot_parser.can_fetch('*', urljoin(
                self.base_url, self.all_job_url)):
            return True
        return False

    @abstractmethod
    def gather_specific_job_info(self, job):
        """
        Ezt a metodust minden scrapernek maganak kell implementalnia, mert
        egy munka leirasanak scrapeleset nem igazan lehet altalanositani
        """
        pass

    def is_cache_outdated(self):
        """
        Megnezzuk, hogy egyaltalan letezik e cache. Ha igen, leszedjuk az
        all job page html tartalmat, ezutan megnezzuk, hogy valtozott-e DE
        ELOBB MEGENZZUK A ROBOTS.txt-t

        CODE SMELL: 2x van az os.remove()
        """
        current_html = requests.get(urljoin(
            self.base_url, self.all_job_url)).text
        soup = BeautifulSoup(current_html, 'html.parser').find(
            self.all_job_container_html_element,
            class_=self.all_job_container_html_class
        )
        with open(
                os.path.join(get_dynamic_parent_folder(
                    self.__class__),
                    '.current.html'),
                'w') as f:
            f.write(str(soup))
        current_html_file = os.path.join(
            get_dynamic_parent_folder(self.__class__),'.current.html')
        if os.path.isfile(self.cache):
            if filecmp.cmp(self.cache, current_html_file):
                os.remove(current_html_file)
                return False
        self.__update_cache(str(soup))
        os.remove(current_html_file)
        return True

    def __update_cache(self, new_data):
        with open(self.cache, 'w') as cache_file:
            cache_file.write(new_data)
