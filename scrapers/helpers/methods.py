from urllib.robotparser import RobotFileParser


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