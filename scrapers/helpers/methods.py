from urllib.robotparser import RobotFileParser

from scrapers.models import URL

def can_fetch_url(robots_url, site_url, useragent="*"):
    """
    Using robots.txt found at robots_url, decides if useragent can fetch
    site url

    :param robots_url: robots.txt url
    :param site_url: to be fetched url
    :param useragent: useragent
    :return: True, if fetching is allowed
    """
    rfp = RobotFileParser()
    rfp.set_url(robots_url)
    rfp.read()
    return rfp.can_fetch(useragent=useragent, url=site_url)


def is_job_already_scraped(url):
    """
    Checks whether the given url is already in the database

    :param url: url of the object
    :return: True, if the given url is already in the database
    """
    try:
        job = URL.objects.get(pk=url)
        return True
    except URL.DoesNotExist:
        return False