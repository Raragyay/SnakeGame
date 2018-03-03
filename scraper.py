import requests
from bs4 import BeautifulSoup
import pprint


def establish_connection(url, urllist):
    my_header = {
        'useragent': 'python-requests/4.8.2(Compatible;raragbot;mailto: raragbot@gmail.com)',
    }
    website = requests.get(url + '/robots.txt', headers=my_header)
    if website.status_code == 200:
        print('{} has accepted your connection! Hooray!'.format(url))
        website = requests.get(url, headers=my_header)
    else:
        if urllist.index(website) == len(urllist):
            print(
                '{} has rejected your connection with a response status code of {}.' \
                'There are no more URLs to try. '.format(url, website.status_code))
        else:
            print('{} has rejected your connection with a response status code of {}.' \
                  'Trying {} next. '.format(url, website.status_code, urllist[urllist.index(url) + 1]))
        website = None
    return website


# I copied this portion of u/Grorco's Github. I was trying to figure out what it did.
def allowed_bots(website):
    allowed = []
    disallowed = []
    isitus = True
    for line in website.text.split('\n'):
        if len(line.split()) == 1: continue
        if line.startswith('User-Agent'):
            if line.split()[1] == '*':
                isitus = True
            else:
                isitus = False
        if line.lower().startswith('allow:') and isitus:
            allowed.append(line.split()[1])
        elif line.lower().startswith('disallow:') and isitus:
            disallowed.append(line.split()[1])

    return allowed, disallowed


def site_dict(urllist):
    sitedict = {}
    for site in urllist:
        website = establish_connection(site + '/robots.txt', urllist)
        if website:
            allowed, disallowed = allowed_bots(website)
            sitedict.update({site: {'allowed': allowed, 'disallowed': disallowed}})
    return sitedict


# Up to here.
def parse_urls(soup):
    results = {}
    for link in soup.find_all('a'):
        string = link.string
        if string:
            try:
                string = ' '.join([i.strip().replace('\n', '') for i in string.split()])
                if link.get('href').startswith('https://') or link.get('href').startswith('http://'):
                    results[string] = link.get('href')
            except AttributeError:
                pass
    return results


urls = [
    'http://www.nasdaq.com',
    'http://www.webscraper.io',
    'https://www.reddit.com'
]
for url in urls:
    website = BeautifulSoup(establish_connection(url, urls).text, 'html.parser')
    if website:
        pprint.pprint(parse_urls(website))
