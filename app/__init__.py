# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: alot

import random
import os
import sqlite3
import sys
from flask import Flask, render_template, request, session, redirect, url_for, flash
# to import matplot lib
import db
import APIs
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import plot

DB_FILE = "db.py"
app = Flask(__name__)

app.secret_key = os.urandom(32)

if (not os.path.isfile("geoTracker.db")):
    db.setup() # sets up databases

@app.route("/", methods=['GET', 'POST'])
def home():
    if 'username' and 'place' in session:
        print(db.getTableData("users", "username", "Ethan"))
        print(session['place'])
        print(session['lon'])
        print(session['lat'])

        #populate db
        beegFile = APIs.fetch_openweather(session['lat'], session['lon'])
        weatherData = beegFile['list']
        db.resetWeather()
        num=0
        for row in weatherData:
            db.logWeather(num, session['username'], session['place'], session['lat'], session['lon'], float(row['main']['temp']), float(row['main']['humidity']), row['weather'][0]['main'], float(row['wind']['speed']))
            num+=1

        #generates plots
        plot.forecast()

        print(db.getWeather())
        return render_template("home.html", username = session['username'], option="5-day forecast", place = session['place'], img_link="static/goo.png")
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
            session['lat'] = float(city_detail[0]['lat'])
            session['lon'] = float(city_detail[0]['lon'])
            return render_template("home.html", username = session['username'], place = session['place'])
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
        session['lat'] = float(city_detail[index]['lat'])
        session['lon'] = float(city_detail[index]['lon'])
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

    earthquake_data = APIs.fetch_earthquake_data(session['username'])
    if earthquake_data:
        for quake in earthquake_data:
            db.logEarthquakes(
                session['username'],
                quake['place'],
                quake['lat'],
                quake['lon'],
                quake['magnitude'],
                quake['depth'],
                quake['description']
            )
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

@app.route("/new_city")
def new_city():
    session.pop('place', None)
    session.pop('lat', None)
    session.pop('lon', None)
    return redirect("/entry")

"""
@app.route("/weather")
def weather():
    '''
    #for testing
    session['username'] = "hi"
    session['place'] = 'london'
    session['lat'] = 51.5073219
    session['lon'] = -0.1276474
    '''

    beegFile = APIs.fetch_openweather(session['lat'], session['lon'])
    weatherData = beegFile['list']
    db.resetWeather()
    num = 0
    for row in weatherData:
        db.logWeather(num, session['username'], session['place'], session['lat'], session['lon'], float(row['main']['temp']), float(row['main']['humidity']), row['weather'][0]['main'], float(row['wind']['speed']))
        num+=1
    plt.figure()
    a = db.getWeather()
    for row in a:
        x = row[0]
        y = row[4]
        plt.plot(x,y,'ro-')
    plt.xlabel("intervals")
    plt.ylabel("temperature")
    plt.tight_layout()

    plt.savefig('static/goo.png')
    print(db.getWeather())
    return render_template("view.html", place = session['place'])
"""

# # This should contain a button to redirect into /history page
@app.route("/history")
def history():
    APIs.fetch_city_pop("Chicago")
    return render_template('history.html')

@app.route("/user_history")
def user_history():
    if 'username' not in session:
        return redirect("/login")
    print(db.getTableData("users", "username", session['username'])[0])
    history_data = db.getAllHistory(db.getTableData("users", "username", session['username'])[0])
    return render_template("user_history.html", username=session['username'], history=history_data)

@app.route("/humidity")
def humidity():
    plot.humidity()
    return render_template("home.html", username = session['username'], option="5-day humidity", place = session['place'], img_link="static/foo.png")

@app.route("/percipitation")
def percipitation():
    plot.percipitation()
    return render_template("home.html", username = session['username'], option="5-day percipitation", place = session['place'], img_link="static/boo.png")



if __name__ == '__main__':
    app.debug = True
    app.run()
