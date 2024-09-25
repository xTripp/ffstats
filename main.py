import logging
import api
from flask import Flask, render_template, request
from datetime import datetime

logging.basicConfig(level=logging.DEBUG)

# Ideas:
# Power rankings graph to display week by week
# Power rankings podium graphics
# Link team names to a team page with specific team stats
# Compare 2 teams stats
# Mini leaderboards by season, all-time, and playoffs
# Luck index
# Live stat command center for live data
# Support tracking other leagues

app = Flask(__name__)
logging.debug("Flask app initialized and starting")

# root route
@app.route('/')
def home():
    logging.debug("Entered '/' route")
    logging.debug("Fetching league data")
    api.league = api.get_league()
    
    current_year = api.league.year
    logging.debug(f"Current year: {current_year}")
    
    logging.debug("Rendering home.html template")
    
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
    logging.debug(f"Current year (system): {current_year}")
    
    logging.debug("Fetching league data for selected year")
    api.league = api.get_league(year)
    
    logging.debug(f"Rendering home.html for year: {year}")
    
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
    logging.debug("Entered '/load_leaderboards' route")
    
    selected_year = request.args.get('year', type=int)
    logging.debug(f"Fetching league data for year: {selected_year}")
    
    api.league = api.get_league(selected_year)
    
    logging.debug("Rendering _leaderboards.html template")
    
    return render_template(
        '_leaderboards.html',
        stats=api.get_league_stats(),
        owners=api.get_league_owners()
    )

# This route is used for render's health checks to prevent it from DOS attacking my site
@app.route('/health')
def health_check():
    return {'status': 'ok'}

if __name__ == "__main__":
    app.run(host='0.0.0.0')
