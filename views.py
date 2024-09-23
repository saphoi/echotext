from app import app
from flask import render_template

@app.route("/")
def menuinicial():
    return render_template("menu.html")

@app.route("/sobrenos")
def sobrenos():
    return render_template("sobre.html")