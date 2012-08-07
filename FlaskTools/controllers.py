from flask import render_template
from FlaskTools import app

@app.route("/")
def index():
    data = dict()
    return "TEST"
#render_template("index.html", data)
