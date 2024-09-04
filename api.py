import os
from dotenv import load_dotenv
from espn_api.football import League

load_dotenv()

def get_league_name():
    league = League(league_id=os.getenv("LEAGUE_ID"), year=2024, espn_s2=os.getenv("ESPN_S2"), swid=os.getenv("SWID"))
    return league.settings.name