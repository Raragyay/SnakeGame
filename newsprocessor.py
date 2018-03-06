def urlify(url, sitename):
    """
    If the url starts with a slash, add on the base url so that it can be properly accessed.
    This is because some urls given by websites start with a slash, since the sites are, after, files.
    It's just like how you don't give the whole file path every time you want to open a file. Do you?
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
    :param stories: Stories that we already have. In the form of a dictionary {headline:link}
    :return: We return that stories, but with some extra links. 
    """
    # TODO: Add a time stamp.
    website_keys = websites[sitename]  # Get the info needed to scrape the website.
    news_stories = soup.find_all(website_keys['block'], {'class': website_keys['class_name']})
    # Find all the headlines.
    foundnews = False
    # We set this to false as default, so that if there is no news, we tell the user that there is no news.
    for news_block in news_stories:
        header = news_block.find(website_keys['header'], {'class': website_keys['header_class']}).text.strip()
        # Get the headline title, to print.
        if header in stories or not header:
            # If the title is already here, or if there is no headline, just go on to the next headline.
            continue
        else:
            foundnews = True
            # No need to print that there was no news anymore.
            print('New from {}! {}'.format(sitename, header))
            link = news_block.find('a').get('href')
            link = urlify(link, sitename)
            # We want to convert it into a proper url, so that it can be printed with nice underlining.
            stories[header] = link
    if not foundnews:
        print('Sorry, no new news from {}.'.format(sitename))
    return stories


websites = {
    'BBC': {
        'block': 'div',  # Blocks are blocks of headlines.
        'class_name': 'gs-c-promo',
        'header': 'h3',  # Header is where we look for the text.
        'header_class': 'gs-c-promo-heading__title',
        'baseurl': 'http://www.bbc.com'  # This is the base url, in case the url starts with a slash.
    },
    'Sky News': {
        'block': 'div',
        'class_name': 'sdc-news-story-grid__card',
        'header': 'h3',
        'header_class': 'sdc-news-story-grid__headline',
        'baseurl': 'https://news.sky.com'
    },
    'The Guardian': {
        'block': 'h2',
        'class_name': 'fc-item__title',
        'header': 'span',
        'header_class': 'js-headline-text',
        'baseurl': 'https://www.theguardian.com'
    }
}
