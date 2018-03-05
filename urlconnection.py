import requests
from bs4 import BeautifulSoup

from custom_exceptions import DisallowedConnection


def isolatebaseurl(url):
    """
    This function isolates the base url, so that the search for robots.txt
    can be properly requested.
    :param url:
    :return: The base url. For example, www.xyz.com/abcde would become www.xyz.com
    """
    urlperiod = url.index('.')
    try:
        urlfirstslash = url[urlperiod:].index('/')
        # Gets the first '/' after the period, which is presumably the .com or .ca or .uk.
    except ValueError:
        # If there is no slash after the period, then it's already the base url
        # Therefore, it is returned in the original form.
        return url
    return url[:urlfirstslash + urlperiod]


def establish_connection(url):
    """
    Uses the requests library to establish a connection with the website, assuming that
    its robots.txt allows it.
    :param url: The URL to be requested.
    :return: The website in raw html form.
    """
    my_header = {
        'useragent': 'python-requests/4.8.2(Compatible;raragbot;mailto: raragbot@gmail.com)',
    }
    baseurl = isolatebaseurl(url)  # Isolate the base url to retrieve the robots.txt.
    robotwebsite = requests.get(baseurl + '/robots.txt', headers=my_header)
    if robotwebsite.status_code == 200:
        # If the robots.txt accepts the connection, go ahead with returning the website.
        print('{} has accepted your connection! Hooray!'.format(url))
        website = requests.get(url, headers=my_header)
        return website
    else:
        # Some websites, like the Economist, reject the connection.
        # Therefore, we raise a custom exception with the status code of the website,
        # so that it can be caught in the run script and stopped.
        raise DisallowedConnection(robotwebsite.status_code)


def soupify(url):
    """
    Converts the raw html form of the website into a soup, which can be parsed properly
    by the Beautiful Soup library.
    :param url: The url. This is used to establish a connection via the
    establish_connection function, then soupified and returned.
    :return: The souped up version of the website
    """
    return BeautifulSoup(establish_connection(url).text, 'html.parser')
