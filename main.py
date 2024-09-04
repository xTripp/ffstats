from flask import Flask, render_template
from api import get_league_name

app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
        'home.html',
        name=get_league_name()
        )

#py -m pip install dotenv
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)