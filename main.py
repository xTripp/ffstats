from flask import Flask, render_template
from api import *

app = Flask(__name__)

@app.route('/')
def home():
    return render_template(
        'home.html',
        name=get_league_name()
    )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)