import pprint

from urlconnection import soupify
import datetime
import pandas as pd


def get_game_stats(game):
    """
    Gets all the stats for the game This includes the name of the team and the score.
    :param game: TODO
    :return: TODO
    """
    df = pd.read_html(str(game), flavor='bs4')[0]
    df.rename(columns=lambda x: x.strip(), inplace=True)
    df.rename(columns={'': 'Teams'}, inplace=True)
    teamnames = df.Teams.values
    for i, team in enumerate(teamnames):
        teamnames[i] = ' '.join([i for i in team.split() if i.lower().islower()])
    df.Teams = teamnames
    return df


def give_wins(winner, loser, dictionary):
    """
    This function adds the correct winners and losers.
    :param winner:
    :param loser:
    :param dictionary:
    :return:
    """
    try:
        dictionary[winner]['wins'] += 1
    except KeyError:
        dictionary[winner] = {'wins': 1, 'losses': 0}
    try:
        dictionary[loser]['losses'] += 1
    except KeyError:
        dictionary[loser] = {'wins': 0, 'losses': 1}
    return dictionary


def basketball_processor(soup, dictionary):
    """
    Plan: To get all match data from past games, including win percentage, individual matchups, and perhaps tournament performance.
    This will involve going through the scoreboards for all past college games
    :param dictionary: This is dictionary
    :param soup: A soupified version of the CBS Sports NCAA Tournament Brackets
    :return: DataFrame
    """
    teams = dictionary.copy()
    games = soup.select('div.single-score-card.postgame')
    for game in games:
        df = get_game_stats(game)
        team_1_score = df.iloc[0, -1]
        team_2_score = df.iloc[1, -1]
        if team_1_score > team_2_score:
            teams = give_wins(df.Teams[0], df.Teams[1], teams)
        elif team_1_score < team_2_score:
            teams = give_wins(df.Teams[1], df.Teams[0], teams)
        print(df)
    return teams


print('15-12'.islower())
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
