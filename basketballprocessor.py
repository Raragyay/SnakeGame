import pprint

from urlconnection import soupify
import datetime


def basketball_processor(soup, dictionary):
    """
    Plan: To get all match data from past games, including win percentage, individual matchups, and perhaps tournament performance.
    This will involve going through the scoreboards for all past college games
    :param dictionary: This is dictionary
    :param soup: A soupified version of the CBS Sports NCAA Tournament Brackets
    :return: DataFrame
    """
    teams = dictionary.copy()
    for teamname in soup.find_all('a', class_='team'):
        if teamname.text not in teams:
            teams[teamname.text] = {'wins': 0, 'losses': 0}
    print(teams)
    games = soup.select('div.single-score-card.postgame')
    win_loss = {}
    for game in games:
        if game.find('div', class_='game-status postgame').text.strip() != 'FINAL':
            continue
        scoretable = game.find('tbody')
        team_1, team_2 = scoretable.find_all('tr', limit=2)
        team_1_name = team_1.find('a', class_='team').text
        team_2_name = team_2.find('a', class_='team').text
        team_1_score = int(team_1.find_all('td')[3].text)
        team_2_score = int(team_2.find_all('td')[3].text)
        if team_1_score > team_2_score:
            teams[team_1_name]['wins'] += 1
            teams[team_2_name]['losses'] += 1
        else:
            teams[team_1_name]['losses'] += 1
            teams[team_2_name]['wins'] += 1
        print(team_1_name, team_1_score)
        print(team_2_name, team_2_score)
    return teams
    # teams = {i.text: {} for i in set(teamnames) if i.text}
    # The dictionary is used to calculate the wins and losses against other teams.
    # return teams

    # regions=tournament.find_all('li',{'class':'region'})
    # teams={}
    # for region in regions:

    # return regions


start_date = datetime.date(2018, 3, 5)
num_of_days = 30
winloss = {}
print(start_date)
for i in range(num_of_days):
    winloss = basketball_processor(
        soupify('https://www.cbssports.com/college-basketball/scoreboard/all/{}'.format(start_date.strftime('%Y%m%d'))),
        winloss)
    start_date -= datetime.timedelta(days=1)

pprint.pprint(winloss)
# https://www.cbssports.com/college-basketball/scoreboard/all/DATE
# Sample link for now: https://www.cbssports.com/college-basketball/scoreboard/all/20180305
# postgame divs, get FIRST table
# Get the two team names, perhaps match them, but if that doesn't work, get the team link profile
# Two rows for the teams
