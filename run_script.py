import time
import newsprocessor as dp
import json
import threading

from custom_exceptions import DisallowedConnection
from urlconnection import soupify


def check_news_site(sitename):
    """
    Check BBC for news stories
    :param sitename: The site name. Used to initiate the whole process.
    :return: Absolutely nothing. It'll write the stuff to a file.
    """
    delay = 10
    maxcount = 5
    stories = loader(sitename)
    for i in range(maxcount):
        print('Checking {} {}'.format(sitename, i + 1))
        dp.news_scraper(soupify(urls[sitename]), sitename, stories)
        time.sleep(delay)
    dumper(stories, sitename)


def dumper(stories, filename):
    with open('{}.txt'.format(filename), 'w') as out:
        json.dump(stories, out)


def loader(filename):
    try:
        with open('{}.txt'.format(filename), 'r') as read:
            stories = json.load(read)
    except (json.decoder.JSONDecodeError, FileNotFoundError):
        return {}
    return stories


urls = {
    'BBC': 'http://www.bbc.com/news',
    'Sky News': 'https://news.sky.com/'
}
try:
    t1 = threading.Thread(target=check_news_site, args=('BBC',))
    t2 = threading.Thread(target=check_news_site, args=('Sky News',))

    t1.start()
    print('Started first thread.')
    t2.start()
    print('Started second thread')

    t1.join()
    t2.join()
    print('Exiting Main Thread.')
except DisallowedConnection as e:
    print('Connection not allowed with HTTP code {}.'.format(e.status))
