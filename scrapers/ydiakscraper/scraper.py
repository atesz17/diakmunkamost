from scrapers.basescraper.scraper import BaseScraper


class YDiakScraper(BaseScraper):

    def gather_specific_job_info(self):
        '''
        Ezt a metodust minden scrapernek maganak kell implementalnia, mert
        egy munka leirasanak scrapeleset nem igazan lehet altalanositani
        '''
        pass
