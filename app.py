from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route("/")
def index():
    return 'Index Page'
@app.route("/about")
def about():
    return 'About Page'

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('index.html', person=name)

with app.test_request_context():
    print(url_for('index'))
    print(url_for('about'))