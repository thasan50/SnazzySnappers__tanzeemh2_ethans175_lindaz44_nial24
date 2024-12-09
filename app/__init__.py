# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

import random
from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import sqlite3
import sys
# import database here
import db
import EarthquakeUSGS
DB_FILE = "db.py"
app = Flask(__name__)

app.secret_key = os.urandom(32)

if (os.path.isfile("geoTracker.db")):
    os.remove("geoTracker.db")
db.setup() # sets up databases

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        print(db.getTableData("users", "username", "Ethan"))
        return render_template("home.html", username = session['username'])
    else:
        return redirect("/login")
#In home, if you receive some input, it should redirect into /view_city page
# Additionally, should include button to move to /natural_disaster
# Button to check /user_history
@app.route('/login', methods=['GET','POST'])
def login():
    return render_template("login.html")

@app.route("/auth_login", methods=['GET', 'POST'])
def auth_login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if db.getUserID(username) >= 0:
            session['username'] = username
            return redirect('/')
        else:
            flash("Incorrect username or password.", 'error')
            return redirect("/login")

@app.route("/earthquake_form", methods=['GET', 'POST'])
def earthquake_form():
    return EarthquakeUSGS.home()

@app.route("/earthquakes_display", methods=['GET', 'POST'])
def earthquake_display():
    return EarthquakeUSFS.get_earthquake_data_by_place()

@app.route("/registration", methods=['GET', 'POST'])
def registration():
    return render_template("registration.html")

@app.route("/auth_registration", methods=['GET', 'POST'])
def auth_registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if db.getUserID(username) >= 0:
            flash("Username already exists", 'error')
            return redirect("/registration")
        else:
            session['username'] = username
            db.addUser(username, password)
            return redirect("/login")

@app.route('/logout', methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    session.pop('name', None)
    return redirect("/")

@app.route("/view_city")
def view():
    return render_template("view.html")
# # This should contain a button to redirect into /history page
@app.route("/history")
def history():
    return render_template('history.html')
@app.route("/natural_disaster")
def disaster():
    return render_template('disaster.html')
@app.route("/user_history")
def user_history():
    return render_template('user_history.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
