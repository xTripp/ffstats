import logging
import api
from flask import Flask, render_template, request, url_for
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

# Ideas:
# Power rankings graph to display week by week
# Link team names to a team page with specific team stats
# Compare 2 teams stats
# Team week grading
# Team points pie chart by position
# Mini leaderboards by season, all-time, and playoffs
# Luck index
# Trade deadline
# Live stat command center for live data
# Support tracking other leagues
# Draft new team or modify existing team and simulate league placement
# Pre-load page content with buffering symbols to show loading immediately
# Support other fantasy platforms

app = Flask(__name__)
logging.debug("Flask app initialized and starting")

# root route
@app.route('/')
def home():
    user_agent = request.headers.get('User-Agent')
    # Give user agent 'Go-http-client/1.1' an ok code instead of loading content
    if 'Go-http-client/1.1' in user_agent:
        logging.debug("Processed request from Go-http-client/1.1")
        return {'status': 'ok'}

    logging.debug("Entered root route")
    api.league = api.get_league()
    
    current_year = api.league.year
    
    return render_template(
        'home.html',
        name=api.get_league_name(),
        selected_season=api.league.year,
        current_year=current_year,
        seasons=api.get_league_seasons(),
        team_count=api.get_league_num_teams(),
        previous_winner=api.get_league_previous_winner(),
        current_week=api.league.current_week,
        power_rankings=api.get_league_power_rankings(),
        trades=api.get_trades()
    )

# When a different season is selected this route is used to generate a new home page with the updated information
@app.route('/<int:year>')
def season_select(year):
    logging.debug(f"Entered '/<int:year>' route with year: {year}")
    
    current_year = datetime.now().year
    api.league = api.get_league(year)
    
    return render_template(
        'home.html',
        name=api.get_league_name(),
        selected_season=year,
        current_year=current_year,
        seasons=api.get_league_seasons(),
        team_count=api.get_league_num_teams(),
        previous_winner=api.get_league_previous_winner(),
        current_week=api.league.current_week,
        power_rankings=api.get_league_power_rankings(),
        trades=api.get_trades()
    )

# This route is used when the user clicks the load leaderboards button to fetch the league stats
@app.route('/load_leaderboards')
def load_leaderboard():
    selected_year = request.args.get('year', type=int)
    api.league = api.get_league(selected_year)

    return render_template(
        '_leaderboards.html',
        stats=api.get_league_stats(),
        owners=api.get_league_owners()
    )

# This route is used to load the luck indices graph for the current season
@app.route('/load_luck')
def load_luck():
    return api.get_luck_indices(api.league, api.league.current_week)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
