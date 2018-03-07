from urlconnection import soupify
import pprint


def get_seeds(soup):
    """
    A small function that gets the seeds in the first round
    :param soup: A soupified version of the url.
    :return: A dictionary: {team_name:{'seed':seed}}
    Pretty much it's a dictionary with the key being the team name, and the value of the dictionary being another dictionary containing the seed.
    """
    team_seeds = {}
    for region in soup.find_all('li', class_='round0'):
        for team in region.find_all('li', class_='team'):
            if not team.text:
                continue
            team_name = team.find('span', class_='name').text
            team_seed = int(team.find('span', class_='seed').text)
            team_seeds[team_name] = {'seed': team_seed}
    return team_seeds


round_0_seeds = get_seeds(
    soupify('https://www.cbssports.com/collegebasketball/ncaa-tournament/brackets/viewable_men'))
sorted_round_0_seeds = sorted(round_0_seeds.items(), key=lambda x: x[1]['seed'])
pprint.pprint(sorted_round_0_seeds)
