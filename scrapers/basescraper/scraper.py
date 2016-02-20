import requests


class BaseScraper:

    def __init__(self, name, all_job_url):
        self.name = name
        self.all_job_url = all_job_url

    def scrape(self):
        pass
