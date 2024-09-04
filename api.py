import os
from dotenv import load_dotenv
from espn_api.football import League

load_dotenv()

"""
Returns a league instance for a specified year.

Parameters: 
    year (int): selects the year of data to get. Defaults to current year
"""
def get_league(year=2024):
    return League(league_id=os.getenv("LEAGUE_ID"), year=year, espn_s2=os.getenv("ESPN_S2"), swid=os.getenv("SWID"))

league = get_league() # Create private leauge instance for use in other functions

"""
Returns name of league
"""
def get_league_name():
    return league.settings.name