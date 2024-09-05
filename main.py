from flask import Flask, render_template
import api

app = Flask(__name__)

@app.route('/')
def home():
    api.league = api.get_league()
    return render_template(
        'home.html',
        name=api.get_league_name(),
        selected_season=api.league.year,
        seasons=api.get_league_seasons(),
        team_count=api.get_league_num_teams(),
        previous_winner=api.get_league_previous_winner()
    )

# When a different season is selected this route is used to generate a new home page with the updated information
@app.route('/season/<int:year>', methods=['GET'])
def season_select(year):
    api.league = api.get_league(year)
    return render_template(
        'home.html',
        name=api.get_league_name(),
        selected_season=year,
        seasons=api.get_league_seasons(),
        team_count=api.get_league_num_teams(),
        previous_winner=api.get_league_previous_winner()
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)