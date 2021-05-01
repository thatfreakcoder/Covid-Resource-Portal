#!/usr/bin/python3.6

from flask import Flask, request, redirect, render_template, flash, url_for, session
from flask_mysqldb import MySQL
from yaml import load, FullLoader
from datetime import datetime 
from os import urandom

app = Flask(__name__)
mysql = MySQL(app)

# MySQL Configuration
db_keeps = load(open('db.yaml'), Loader=FullLoader)
app.config['MYSQL_HOST'] = db_keeps['mysql_host']
app.config['MYSQL_USER'] = db_keeps['mysql_user']
app.config['MYSQL_PASSWORD'] = db_keeps['mysql_password']
app.config['MYSQL_DB'] = db_keeps['mysql_db']
app.config['SECRET_KEY'] = urandom(24)

CLASSES = ["success", "danger", "primary", "info", "warning", "dark"]

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM resources ORDER BY res_id DESC;")
    if q > 0:
        resources = cur.fetchall()
        return render_template('index.html', resources=resources, classes=CLASSES)
    else:
        return render_template('index.html', resources=None)

@app.route('/new/', methods=['GET', 'POST'])
def post():
    if request.method == 'POST':
        result = request.form
        description = str(result['description'])
        date_time = str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        tags = str(request.form.getlist('tags'))[1:-1].replace("'", "")
        location = str(result['location']).lower()
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO resources(description, datetime, tags, location) VALUES( %s, %s, %s, %s);", (description, date_time, tags, location))
        mysql.connection.commit()
        cur.close()
        flash("Thank You for your contribution.", "success")
        return redirect('/')
    return render_template('new.html')

@app.route('/search/locations')
def search_location():
    location = str(request.args.get('q')).lower()
    cur = mysql.connection.cursor()
    q = cur.execute("SELECT * FROM resources WHERE location='{}';".format(location))
    if q > 0:
        resources = cur.fetchall()
        return render_template('index.html', resources=resources, classes=CLASSES)
    else:
        return render_template('index.html', resources=None)

@app.route('/search/tags')
def search_tag():
    tags = str(request.args.get('q')).upper().split(' ')
    print(tags)
    cur = mysql.connection.cursor()
    for tag in tags:
        q = cur.execute("SELECT * FROM resources WHERE tags LIKE '%{}%';".format(tag))
        if q > 0:
            resources = cur.fetchall()
            return render_template('index.html', resources=resources, classes=CLASSES)
        else:
            return render_template('index.html', resources=None)

@app.route('/admin/success/', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form.get('password') == 'admin@covidhelp123':
            session['logged_in'] = True
            flash("Admin Access Granted", "success")
        else:
            flash("Incorrect Password", "danger")
            session['logged_in'] = False
        return redirect('/admin/success/')
    else:
        return render_template('admin.html')

@app.route('/admin/')
def success():
    session['logged_in'] = False
    return render_template('admin.html')

@app.errorhandler(404)
def error(err):
    return render_template('404.html')

if __name__ == '__main__':
    app.run(debug=True)