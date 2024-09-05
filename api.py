import os
from dotenv import load_dotenv
from datetime import datetime
from espn_api.football import League

load_dotenv()

# TODO get league is going to have to be rewritten to allow changing league year for re-rendering page
"""
Returns a league instance for a specified year. If the year is not a year the league was active it will return None

Parameters: 
    year (int): selects the year of data to get. Defaults to current year
"""
def get_league(year=datetime.now().year):
    try:
        return League(league_id=os.getenv("LEAGUE_ID"), year=year, espn_s2=os.getenv("ESPN_S2"), swid=os.getenv("SWID"))
    except:
        return None

league = get_league()  # Create private leauge instance for use in other functions

"""
Returns (str) name of league
"""
def get_league_name():
    return league.settings.name

"""
Returns (list) all league seasons by year
"""
def get_league_seasons():
    year = datetime.now().year
    # append the current year if not already in the list
    if year not in league.previousSeasons:
        league.previousSeasons.append(year)
    return league.previousSeasons

"""
Returns (int) number of teams in league
"""
def get_league_num_teams():
    return league.settings.team_count

"""
Returns (tuple) the previous league winner's team info. If there is no previous winner it will return None
Ex. (Name, (Wins, Ties, Loses))
"""
def get_league_previous_winner():
    last_league = get_league(datetime.now().year - 1)
    if last_league == None:
        return None
    for team in last_league.teams:
        if team.final_standing == 1:
            return (team.team_name, (team.wins, team.ties, team.losses))
        