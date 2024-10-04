from app import app
from flask import render_template

@app.route("/")
def menuinicial():
    return render_template("index.html")

@app.route("/about")
def sobrenos():
    return render_template("about.html")
