#!/usr/bin/env python

import flask
import pymongo
import config
app = flask.Flask(__name__)
app.config.from_object(config)

db = pymongo.Connection(config.MONGOLAB_URI)

@app.route('/')
def index():
    return flask.render_template("index.html")

if __name__ == '__main__':
    app.run()


