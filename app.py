#!/usr/bin/python3.6

from flask import Flask, request, jsonify, render_template
from flask_mysqldb import MySQL
from os import urandom
from yaml import load, FullLoader

app = Flask(__name__)
mysql = MySQL(app)

# MySQL Configuration
db_keeps = load(open('db.yaml'), Loader=FullLoader)
app.config['MYSQL_HOST'] = db_keeps['mysql_host']
app.config['MYSQL_USER'] = db_keeps['mysql_user']
app.config['MYSQL_PASSWORD'] = db_keeps['mysql_password']
app.config['MYSQL_DB'] = db_keeps['mysql_db']
app.config['SECRET_KEY'] = urandom(24)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM resources ORDER BY res_id DESC;")
    if q > 0:
        resources = cur.fetchall()
        return render_template('index.html', resources=resources)
    else:
        return render_template('index.html', resources=None)

if __name__ == '__main__':
    app.run(debug=True)