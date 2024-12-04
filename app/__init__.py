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
def register():
    return render_template("registration.html")
# # Leave empty for Nia to do
# @app.route("/view_city")
#
# # This should contain a button to redirect into /history page
# @app.route("/history")
#
# @app.route("/natural_disaster")
#
# @app.route("/user_history")


if __name__ == '__main__':
    app.debug = True
    app.run()
