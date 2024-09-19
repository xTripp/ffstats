import api
from flask import Flask, render_template, request

# Ideas:
# Power rankings graph to display week by week
# Link team names to a team page with specific team stats
# Compare 2 teams stats
# Mini leaderboards by season, all-time, and playoffs
# Trade tracker
# Luck index

app = Flask(__name__)

# root route
@app.route('/')
def home():
    api.league = api.get_league()
    return render_template(
        'home.html',
        name=api.get_league_name(),
        selected_season=api.league.year,
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
    api.league = api.get_league(year)
    return render_template(
        'home.html',
        name=api.get_league_name(),
        selected_season=year,
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
    api.league = api.get_league(request.args.get('year', type=int))
    return render_template(
        '_leaderboards.html',
        stats=api.get_league_stats(),
        owners=api.get_league_owners()
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)