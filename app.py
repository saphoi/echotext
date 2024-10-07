from flask import Flask

app = Flask(__name__, template_folder='templates')

from views import *

if __name__ == "__main__":
    app.run()