def urlify(url, sitename):
    """
    If the url starts with a slash, add on the base url so that it can be properly accessed.
    :param url:
    :param sitename:
    :return: The nicely formatted url.
    """
    if url.startswith('/'):
        url = websites[sitename]['baseurl'] + url
    return url


def news_scraper(soup, sitename, stories):
    """
    Scrape news stories from whatever site you please.
    :param sitename: The site name. Used to reference the dictionaries.
    :param soup: The soupified version of the website.
    :param stories: Stories that we already have. In the form of a dictionary {header:link}
    :return: We return that stories, but with some extra links. 
    """
    newsclass = websites[sitename]
    news_stories = soup.find_all(newsclass['block'], {'class': newsclass['classname']})
    foundnews = False
    for news_block in news_stories:
        header = news_block.find('h3').string
        if header in stories or not header:
            continue
        else:
            foundnews = True
            print('New from {}! {}'.format(sitename, header))
            link = news_block.find('a').get('href')
            link = urlify(link, sitename)
            stories[header] = link
    if not foundnews: print('Sorry, no new news.')
    return stories


websites = {
    'BBC': {
        'block': 'div',
        'classname': 'gs-c-promo',
        'baseurl': 'http://www.bbc.com/news'
    },
    'CNN': {
        'block': 'article',
        'classname': 'cd',
        'baseurl': 'https://www.cnn.com'
    }
}
