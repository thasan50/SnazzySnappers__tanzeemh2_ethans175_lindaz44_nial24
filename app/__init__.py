# SnazzySnapeprs - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

import random
import db
from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import sqlite3
import sys
# import database here
import db

DB_FILE = "db.py"
app = Flask(__name__)

app.secret_key = os.urandom(32)

if (os.path.isfile("geoTracker.db")):
    os.remove("geoTracker.db")
db.setup() # sets up databases

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template("home.html", user = session['username'])
    else:
        return redirect("/registration")
#In home, if you recieve some input, it should redirect into /view_city page
# Additionally, should include button to move to /natural_disaster
# Button to check /user_history
@app.route("/registration")
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db.addUser(username, password)
        session['username'] = username

        return redirect("/")
    else:
        return render_template(url_for('registraton.html')
# # Leave empty for Nia to do
@app.route("/view_city")
def view():

    return render_template("view.html");
# # This should contain a button to redirect into /history page
@app.route("/history")
def history():
    return render_template('history.html');
@app.route("/natural_disaster")
def disaster():
    return render_template('disaster.html');
@app.route("/user_history")
def user_history():

    return render_template('user_history.html');

if __name__ == '__main__':
    app.debug = True
    app.run()
