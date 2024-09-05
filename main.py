from flask import Flask, render_template
from api import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
        'home.html',
        name=get_league_name(),
        seasons=get_league_seasons(),
        team_count=get_league_num_teams(),
        previous_winner=get_league_previous_winner()
    )

# When a different season is selected this route is used to refresh the home page with the new season information
# TODO fix this whole redirect mess, might be best to re-render home with the new values after resetting the league in api
@app.route('/season_select')
def season_select():
    return home()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)