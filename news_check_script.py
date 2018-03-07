import time
import newsprocessor as dp
import threading
import jsoninterchange
from custom_exceptions import DisallowedConnection
from urlconnection import soupify


def check_news_site(sitename):
    """
    Check the news sites for news stories. Of course, the condition has to be that they are in the url list.
    :param sitename: The site name. Used to initiate the whole process.
    :return: Absolutely nothing. It'll write the stuff to a file.
    """
    delay = 10
    maxcount = 5
    stories = jsoninterchange.loader(sitename)
    for i in range(maxcount):
        print('Checking {} {}'.format(sitename, i + 1))
        dp.news_scraper(soupify(urls[sitename]), sitename, stories)
        time.sleep(delay)
    jsoninterchange.dumper(stories, sitename)


urls = {
    'BBC': 'http://www.bbc.com/news',
    'Sky News': 'https://news.sky.com/',
    'The Guardian': 'https://www.theguardian.com/international'
}

threads = []
for key in urls:
    threads.append(threading.Thread(target=check_news_site, args=(key,)))
for index, thread in enumerate(threads):
    try:
        print('Started thread {}'.format(index + 1))
        thread.start()
    except DisallowedConnection as e:
        print('Connection not allowed with HTTP code {}.'.format(e.status))
for thread in threads:
    if thread.is_alive():
        thread.join()
print('Exiting Main Thread.')
