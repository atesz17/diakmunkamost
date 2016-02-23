import configparser

import requests


class BaseScraper:
    '''
    Minden scrapernek ez lesz ay ososztalya
    Lehetosing szerint az automatizalhato dolgokat mint pl.: url-ek scrapelese,
    json kiirasa, cache osszehasonlitasa, ezeket itt megvlaositom, a
    specifikusabb reszeket pedig majd az alosztalyban. Lenyeges dolgokat
    egy config fajlbol fogja kiolvasni
    '''

    def __init__(self, config_file="scraper.ini"):
        self.__read_configuration(configparser.ConfigParser(config_file))

    def __read_configuration(self, config):
        '''
        Azoknal az ertekeknel, ami mindenkeppen specifikus, ott a [] operatort
        kell hasznalni, ahol elkepzelheto deafult value, ott a get()-et
        '''
        self.name = self.config['Name']
        self.all_job_url = self.config['AllJobUrl']
        self.cache = self.config.get('Cache', 'cache.html')
        self.jobs_json = self.config.get('JSON', 'scraped_jobs.json')

    def scrape(self):
        pass
