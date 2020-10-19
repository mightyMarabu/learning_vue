
import sqlite3

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
##### sqlite
# sqlite-db
@app.route("/getData/")
def getData():
    connect = sqlite3.connect('learning_vue/app/db.sqlite')
    cur = connect.cursor()
    #c.execute("create table hello_world(id int, text text);")
    #c.execute("insert into hello_world(id,text) VALUES (1,'Hello World');")
    cur.execute("select * from hello_world;")
    result = cur.fetchall()
    connect.commit()
    connect.close()
    return Response(json.dumps(result), mimetype="application/json")
   


#####################################################################
if __name__ == "__main__":
    app.run(debug = True)
    app.run(host='0.0.0.0', port=80)
