from flask import render_template
from web import app

@app.route("/")
def index():
    return render_template("home.html")