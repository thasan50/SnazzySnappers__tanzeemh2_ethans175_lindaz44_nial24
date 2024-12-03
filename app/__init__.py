# SnazzySnapeprs - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

import random, db
from flask import Flask, render_template, request, session, redirect, url_for, flash
import os
import sqlite3
import sys
# import database here
import db
DB_FILE = "db.py"
app = Flask(__name__)

app.secret_key = os.urandom(32)

db.setup() # sets up databases

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' in session:
        return render_template("home.html", user = session['username'])
    else:
        return redirect("/registration")

@app.route("/registration")

@app.route("/view_city")

@app.route("/history")

@app.route("/natural_disaster")

@app.route("/user_history")
if __name__ == "__main__":
    app.debug = True
    app.run()
