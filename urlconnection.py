import requests
from bs4 import BeautifulSoup

from custom_exceptions import DisallowedConnection


def isolatebaseurl(url):
    urlperiod = url.index('.')
    try:
        urlfirstslash = url[urlperiod:].index('/')
    except ValueError:
        return url
    return url[:urlfirstslash + urlperiod]


def establish_connection(url):
    """

    :param url:
    :return: The Website.
    """
    my_header = {
        'useragent': 'python-requests/4.8.2(Compatible;raragbot;mailto: raragbot@gmail.com)',
    }
    baseurl = isolatebaseurl(url)
    robotwebsite = requests.get(baseurl + '/robots.txt', headers=my_header)
    if robotwebsite.status_code == 200:
        print('{} has accepted your connection! Hooray!'.format(url))
        website = requests.get(url, headers=my_header)
        return website
    else:
        raise DisallowedConnection(robotwebsite.status_code)


def soupify(url):
    """

    :param url:
    :return: The souped up version of the website
    """
    return BeautifulSoup(establish_connection(url).text, 'html.parser')
