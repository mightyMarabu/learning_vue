

from flask import Flask, render_template, request, Response, jsonify
import markdown.extensions.fenced_code

from db_conn import *

import json


app = Flask(__name__)
### index ###
@app.route("/")
def index():
    return render_template('index.html')

####### ?? ###########################################################
@app.route("/db_sync/", methods=['GET', 'POST'])
def DBsync():
    executeDBsync()
    return jsonify("DB syncronised")

if __name__ == "__main__":
    app.run(debug = True)
    app.run(host='0.0.0.0', port=80)
