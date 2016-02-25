from abc import ABCMeta, abstractmethod
import configparser
import os
import inspect

import requests


class BaseScraper(metaclass=ABCMeta):
    '''
    Minden scrapernek ez lesz az ososztalya
    Lehetosing szerint az automatizalhato dolgokat mint pl.: url-ek scrapelese,
    json kiirasa, cache osszehasonlitasa, ezeket itt megvlaositom, a
    specifikusabb reszeket pedig majd az alosztalyban. Lenyeges dolgokat
    egy config fajlbol fogja kiolvasni
    '''

    def __init__(self, config_file_name="scraper.ini"):
        config_file = os.path.join(self.get_parent_folder(), config_file_name)
        config = configparser.ConfigParser()
        config.read(config_file)
        self.__read_configuration(config)

    def get_parent_folder(self):
        return os.path.dirname(inspect.getfile(self.__class__))

    def __read_configuration(self, config):
        '''
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
        - jobs_json: scrapelt adatok, ezek mennek majd tovabb a converternek
        '''
        config = config['DEFAULT']
        self.provider_name = config['ProviderName']
        self.all_job_url = config['AllJobUrl']
        self.all_job_container_html_tag = config['AllJobContainerHtmlTag']
        self.single_job_html_tag = config['SingleJobHtmlTag']
        self.cache = config.get('Cache', 'cache.html')
        self.jobs_json = config.get('JSON', 'scraped_jobs.json')

    def scrape(self):
        if self.is_cache_outdated():
            self.gather_info()

    @abstractmethod
    def gather_specific_job_info(self):
        '''
        Ezt a metodust minden scrapernek maganak kell implementalnia, mert
        egy munka leirasanak scrapeleset nem igazan lehet altalanositani
        '''
        pass

    def is_cache_outdated(self):
        '''
        Megnezzuk, hogy egyaltalan letezik e cache. Ha igen, leszedjuk az
        all job page html tartalmat, ezutan megnezzuk, hogy valtozott-e DE
        ELOBB MEGENZZUK A ROBOTS.txt-t
        '''
        if self.robots_are_forbidden():
            pass  # TODO
        current_html = requests.get(self.all_job_url).text
        if os.path.isfile(self.cache):
            with open(self.cache) as cache_file:
                cache_html = cache_file.read()
                if current_html == cache_html:
                    return False
        self.__update_cache(current_html)
        return True

    def __update_cache(self, new_data):
        with open(self.cache, 'w') as cache_file:
            cache_file.write(new_data)
