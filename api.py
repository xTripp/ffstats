import os
import json
import io
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import send_file
from espn_api.football import League
from leaderboardBuilder import LeaderboardBuilder
from utils.luck_index import set_league_endpoint, get_roster_settings, get_season_luck_indices

load_dotenv()
league = League
with open('nfl_start_dates.json', 'r') as file:
    nfl_start_dates = json.load(file)

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
Returns (list[tuple]) the power rankings for any week. Each tuple is ()

Parameters: 
    week (int): selects the week of data to get. Defaults to current week if not provided
"""
def get_league_power_rankings(week=None):
    if week is None:
        week = league.current_week

    # This appends the rank change week over week to the owner's power ranking score
    # The try/except block will prevent an error if its Week 0 and it is checking for a week before that
    try:
        previous_week = league.power_rankings(week - 2)  # not sure why this needs to be -2 but it doesn't get the right rankings with -1
        current_week = league.power_rankings(week)

        # Iterate over all teams and check their rankings from the previous week to calculate rank change
        for i, (_, current_team) in enumerate(current_week):
            previous_team_rank = next(j for j, (_, team) in enumerate(previous_week) if team == current_team)
            rank_change = previous_team_rank - i

            current_week[i] = [current_week[i], rank_change]

        return current_week
    except:
        return league.power_rankings(week)

"""
Returns (dict) of dicts where each is a leaderboard for a different stat. See leaderboardBuilder class for specific information on stat fields
"""
def get_league_stats():
    return LeaderboardBuilder(league).leaderboards

"""
Returns (dict) keyed by team name with a value of a formatted string of the team owners names
"""
def get_league_owners():
    owners = {}
    for team in league.teams:
        owners[team.team_name] = _name_builder(team.owners)

    return owners

"""
Returns (string) owners names for a team

Parameters:
    owners (array): owners of the team
"""
def _name_builder(owners):
    if len(owners) == 1:
        return owners[0]['firstName'] + " " + owners[0]['lastName']
    elif len(owners) == 2:
        return f"{owners[0]['firstName']} {owners[0]['lastName']} and {owners[1]['firstName']} {owners[1]['lastName']}"
    else:
        return f"{', '.join(owner['firstName'] + ' ' + owner['lastName'] for owner in owners[:-1])}, and {owners[-1]['firstName']} {owners[-1]['lastName']}"

"""
This function is responsible for gathering all trades within the given season and passing a dictionary of every trade with information of the assets traded.

Returns:
    trades (dict): A dict keyed by the trade date in epoch (ms) time in UTC and the value of another dict containing the week the trade occurred, the assets given from both sides of the trade as well as the points each asset scored since the trade date. The actions attribute of the trade is also passed for extra information
"""
def get_trades():
    trades = {}

    # If the season selected is not the current season, this will error out and say the league does not exist. In that case, return trades as None type
    try:
        for trade in league.recent_activity(size=1000, msg_type="TRADED"):
            actions = sorted(trade.actions, key=lambda x: x[0].team_name)
            trade_week = _get_week(trade.date)

            team1 = actions[0][0]
            team2 = actions[-1][0]
            
            team1_assets = [asset[2] for asset in actions if asset[0].team_name == team1.team_name]
            team2_assets = [asset[2] for asset in actions if asset[0].team_name == team2.team_name]

            # Calculate total points for each player from the trade week onwards
            team1_points = {asset: sum(week.get('points', 0) for week_key, week in asset.stats.items() if week_key >= trade_week) for asset in team1_assets}
            team2_points = {asset: sum(week.get('points', 0) for week_key, week in asset.stats.items() if week_key >= trade_week) for asset in team2_assets}
            
            # Assets and points are backwards to place the received assets on the correct side
            trades[trade.date] = {
                'week': trade_week,
                'team1_assets': team2_assets,
                'team2_assets': team1_assets,
                'team1_points': team2_points,
                'team2_points': team1_points,
                'actions': actions
            }
    except:
        return None
    
    # bug fix for vu being a bad commissioner, remove at end of season
    trades.pop(1727311997623)
    trades.pop(1727308876229)

    return trades

"""
Generates the league luck index for all teams
NOTE: This currently uses a luck index calculation from (https://github.com/DesiPilla/espn-api-v3/tree/master) it is kind of ripped out and shoved into place so a little scuffed
NOTE: Eventually I want to do my own calculations for this

Parameters:
    league (League): League object for current season
    current_week (int): current week of the season to calculate luck index to this week

Returns:
    luck_indices (dict): A dictionary keyed by Team objects and the value is the luck index
"""
def get_luck_indices(league, current_week):
    league.cookies = {"swid": os.getenv("SWID"), "espn_s2": os.getenv("ESPN_S2")}
    set_league_endpoint(league)
    get_roster_settings(league)
    luck_indices = dict(sorted(get_season_luck_indices(league, current_week).items(), key=lambda item: float(item[1])))

    # Convert Team objects to strings for the x-axis labels
    teams = [team.team_name for team in luck_indices.keys()]
    values = list(luck_indices.values())

    img = _generate_luck_graph(teams, values)

    return send_file(img, mimetype='image/png')

"""
Gets the week for and action in any given season since 2002

Parameters:
    time (int): epoch time for the action to get the week of

Retruns:
    week (int): week of the action
"""
def _get_week(time):
    season_start_in_seconds = nfl_start_dates[str(league.year)] / 1000
    action_time_in_seconds = time / 1000

    # subtract 1 day from season start to align with the start of the new week in ESPN Fantasy
    season_start_time = datetime.fromtimestamp(season_start_in_seconds) - timedelta(days=1)
    action_time = datetime.fromtimestamp(action_time_in_seconds)

    # if the action time is before the first week, it will return 0th week
    if action_time < season_start_time:
        return 0

    delta = action_time - season_start_time

    return (delta.days // 7) + 1

def _generate_luck_graph(teams, values):
    plt.style.use('seaborn-v0_8-dark')
    
    # Create the bar plot
    fig, ax = plt.subplots(figsize=(10, 6))

    # Define the y-axis limits to show from -1.25 to 1.25
    ax.set_ylim(-1.25, 1.25)

    # Draw bars, where bars below 0 will be displayed downwards, and above 0 upwards
    bars = ax.bar(teams, values, color=['#FF6F61' if v < 0 else '#6BAED6' for v in values], edgecolor='black')

    # Add a horizontal line at y=0
    ax.axhline(0, color='black', linewidth=1.2)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right', fontsize=10)
    ax.xaxis.set_tick_params(pad=20)

    # Set axis labels
    ax.set_ylabel('Luck Index', fontsize=12, weight='bold')

    # Enable horizontal grid lines only
    ax.yaxis.grid(True, which='major', linestyle='--', linewidth=0.5, alpha=0.7, color="black")

    # Add labels on top of bars
    for bar, value in zip(bars, values):
        height = bar.get_height()
        ax.annotate(f'{value:.2f}', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 5 if height >= 0 else -15),  # Position above/below the bar
                    textcoords="offset points", ha='center', va='bottom' if height >= 0 else 'top', fontsize=9)

    # Save the plot to a BytesIO object with a transparent background
    img = io.BytesIO()
    plt.tight_layout(pad=2)
    plt.savefig(img, format='png', transparent=True)  # Set transparent=True for transparent background
    plt.close(fig)  # Close the figure to release memory
    img.seek(0)

    return img
