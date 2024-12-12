# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

import random
import os
import sqlite3
import sys
from flask import Flask, render_template, request, session, redirect, url_for, flash
# to import matplot lib
import db
import APIs
import json

DB_FILE = "db.py"
app = Flask(__name__)

app.secret_key = os.urandom(32)

if (os.path.isfile("geoTracker.db")):
    os.remove("geoTracker.db")
db.setup() # sets up databases

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' and 'place' in session:
        print(db.getTableData("users", "username", "Ethan"))
        print(session['place'])
        print(session['lon'])
        print(session['lat'])
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
            if not('place' in session):
                return redirect("/entry")
            return redirect('/')
        else:
            flash("Incorrect username or password.", 'error')
            return redirect("/login")

@app.route("/entry", methods=['GET', 'POST'])
def entry():
    if not 'username' in session:
        return redirect("/login")

    if request.method == 'POST':
        print(request.form)
        location = request.form.get('place')
        session['submittedPlace'] = location
        city_detail = APIs.possible_city(location)
        if city_detail is None:
            flash("error getting data", 'error')
            return render_template("entry.html")

        if(len(city_detail)==0): #no matching city
            flash("Enter another city", 'error')
            return render_template("entry.html")
        if(len(city_detail)==1): #user entered city matches one in api
            session['place'] = city_detail[0]['name']
            session['lat'] = city_detail[0]['lat']
            session['lon'] = city_detail[0]['lon']
            return render_template("home.html", username = session['username'])
        else:
            #if there are multiple cities with same name
            all_city = ""
            index = 0
            print(city_detail)
            for city in city_detail:
                if "state" in city:
                    state = city['state']
                else:
                    state = "none"
                all_city+=(f'''<input type="radio" id="{city['lat']}" name="place" value={index} required> <label for="{city['lat']}"> {city['name']}, {state}, {city['country']}</label>''')
                index+=1
            return render_template("entry_multiple.html", cities=all_city)

    return render_template("entry.html")

@app.route("/entry_choose", methods=['GET', 'POST'])
def match():
    if not 'submittedPlace' in session:
        return render_template("entry.html")
    if request.method=='POST':
        city_detail = APIs.possible_city(session['submittedPlace'])
        index = int(request.form.get('place'))
        session['place'] = city_detail[index]['name']
        session['lat'] = city_detail[index]['lat']
        session['lon'] = city_detail[index]['lon']
        return redirect("/")
    return render_template("entry_multiple.html", cities=all_city)


@app.route("/earthquake", methods=['GET', 'POST'])
def earthquake_form():
    if 'username' not in session:
        return redirect('/')
    return render_template("earthquake.html")

@app.route("/earthquake_display", methods=['GET', 'POST'])
def earthquake_display():
    if 'username' not in session:
        return redirect('/')
    APIs.fetch_earthquake_data(session['username'])
    print(db.getTableData("earthquakes", "location_name", "California"))

    return render_template('earthquake_display.html')

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
    session.pop('place', None)
    return redirect("/login")

@app.route("/view_city")
def view():
    APIs.fetch_city_pop("San Francisco")
    return render_template("view.html")
# # This should contain a button to redirect into /history page
@app.route("/history")
def history():
    return render_template('history.html')

@app.route("/user_history")
def user_history():
    return render_template('user_history.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
