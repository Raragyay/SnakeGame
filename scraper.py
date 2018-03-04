import requests
from bs4 import BeautifulSoup
import pandas as pd
from custom_exceptions import DisallowedConnection

pd.set_option('expand_frame_repr', False)


# pd.set_option('max_rows',500)

def establish_connection(url, urllist):
    my_header = {
        'useragent': 'python-requests/4.8.2(Compatible;raragbot;mailto: raragbot@gmail.com)',
    }
    website = requests.get(url + '/robots.txt', headers=my_header)
    if website.status_code == 200:
        print('{} has accepted your connection! Hooray!'.format(url))
        website = requests.get(url, headers=my_header)
    else:
        if urllist.index(url) == len(urllist) - 1:
            print(
                '{} has rejected your connection with a response status code of {}. ' \
                'There are no more URLs to try. '.format(url, website.status_code))
        else:
            print('{} has rejected your connection with a response status code of {}. ' \
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
        try:
            website = establish_connection(site, urllist)
        except DisallowedConnection as e:
            print('Connection to {} not allowed with HTTP code {}. Does its robots.txt allow access?'.format(site,
                                                                                                             e.status))
            continue
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


def get_players(table, initials, teams):
    df = pd.read_html(str(table), flavor='bs4', attrs={'id': 'rank-data'}, skiprows=[1])[0]
    df.rename(columns={'Overall (Teams)': 'Full Name'}, inplace=True)
    df = df.drop(['WSID', 'Bye', 'Rank', 'Notes'], axis=1)  # Remove all the unnecessary columns
    df = df[df['Pos'].notnull()]  # Remove the 'Tiers' and Google Ads
    df.insert(1, 'Team', teams)
    df.insert(1, 'Initials', initials)
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    print(df)
    print(df.describe())


urls = [
    'http://www.nasdaq.com',
    'http://www.webscraper.io',
    'https://www.reddit.com',
    'http://www.elitettc.ca'
]

dataurls = [
    'https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php'
]
# for url in urls:
#    website = establish_connection(url, urls)
#    if website:
#        soup = BeautifulSoup(website.text, 'html.parser')
#        pprint.pprint(parse_urls(soup))

for url in dataurls:
    website = establish_connection(url, dataurls)
    if website:
        soup = BeautifulSoup(website.text, 'html.parser')
        table = soup.find_all('table')[0]
        initialslist = []
        teamslist = []
        for player in table.find_all('tr', {'class': 'player-row'}):
            link = player.find('a', href=True)
            if 'teams' in link.get('href'):  # That's not a player, that's a team!
                player.decompose()
            else:  # If it's not an imposter, then I delete the initials and team names, and move them to a seperate list to be inserted later on.
                initials = player.find('span', {'class': 'short-name'})
                team = player.find('small', {'class': 'grey'})
                initialslist.append(initials.string)
                teamslist.append(team.string)
                initials.decompose()
                team.decompose()
        get_players(table, initialslist, teamslist)
