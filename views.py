from app import app
from flask import render_template

@app.route("/")
def menuinicial():
    return render_template("menuinicial.html")

@app.route("/sobrenos")
def sobrenos():
    return render_template("sobrenos.html")