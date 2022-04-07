import flask


app = flask.Flask(__name__)

from Routes import *

if __name__ == "__main__":
    app.run(port=8080, host='127.0.0.1')