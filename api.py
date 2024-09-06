import os
from dotenv import load_dotenv
from datetime import datetime
from espn_api.football import League
from leaderboardBuilder import LeaderboardBuilder

load_dotenv()
league = League

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

"""
Returns (str) name of league
"""
def get_league_name():
    return league.settings.name

"""
Returns (list[int]) all league seasons by year
"""
def get_league_seasons():
    current_league = get_league()

    # append the current year if not already in the list
    if current_league.year not in current_league.previousSeasons:
        current_league.previousSeasons.append(current_league.year)
    
    return current_league.previousSeasons

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
    last_league = get_league(league.year - 1)
    if last_league == None:
        return None
    for team in last_league.teams:
        if team.final_standing == 1:
            return (team.team_name, (team.wins, team.ties, team.losses))

"""
Returns (list[tuple]) the power rankings for any week

Parameters: 
    week (int): selects the week of data to get. Defaults to current week if not provided
"""
def get_league_power_rankings(week=None):
    if week == None:
        week = league.current_week
    return league.power_rankings(week)

def get_league_stats():
    return LeaderboardBuilder(league).stats
        