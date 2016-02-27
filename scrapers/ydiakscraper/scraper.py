from scrapers.basescraper.scraper import BaseScraper

from bs4 import BeautifulSoup


class YDiakScraper(BaseScraper):

    def gather_specific_job_info(self, job):
        """
        Ezt a metodust minden scrapernek maganak kell implementalnia, mert
        egy munka leirasanak scrapeleset nem igazan lehet altalanositani

        Egyelore csak pesti munkakat parsolunk, szval alapbol visszaterunk,
        ha nem pesti munkarol van szo
        """
        soup = BeautifulSoup(job, 'html.parser')
        self.job_attrs['place_of_work'] = soup.find(
            itemprop="addressRegion").get_text()
        #  csunya a beegetett ertek, egyelore csak pesti munkak erdekelnek
        if not 'pest' in self.job_attrs['place_of_work'].lower():
            return
        self.job_attrs['title'] = soup.find(itemprop="title").get_text()
        self.job_attrs['job_type'] = soup.find(
            itemprop="occupationalCategory").get_text()
        self.job_attrs['task'] = soup.find(
            itemprop="responsibilities").get_text()
        self.job_attrs['requirements'] = soup.find(
            itemprop="qualifications").get_text()
        self.job_attrs['working_hours'] = soup.find(
            itemprop="workHours").get_text()
        self.job_attrs['salary'] = soup.find(itemprop="baseSalary").get_text()
        self.job_attrs['other'] = soup.find(
            itemprop="baseSalary").find_next('p').get_text()
        print('')
