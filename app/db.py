# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

import sqlite3
import csv
from datetime import datetime

DB_FILE = "geoTracker.db"

def setup():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    # main difference from DD is the integer primary key that autoincrements for each database
    # these are unique per DB, but the DBs are still connected through userID and search_type
    # note that we may want to create another column to detail the timestamps of the data itself from the APIs
    c.execute("CREATE TABLE users (user_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, created_at TEXT, last_login TEXT);")
    c.execute("CREATE TABLE userHistory (history_id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, search_type TEXT, search_time TEXT);")
    c.execute("CREATE TABLE weather (weather_id INTEGER PRIMARY KEY AUTOINCREMENT, location_name TEXT, latitude REAL, longitude REAL, temperature REAL, humidity INTEGER, precipitation REAL, wind_speed REAL, search_time TEXT);")
    c.execute("CREATE TABLE weatherHistory (history_id INTEGER PRIMARY KEY AUTOINCREMENT, location_name TEXT, latitude REAL, longitude REAL, year INTEGER, avg_temperature REAL, avg_precipitation REAL, high_temperature REAL, low_temperature REAL, search_time TEXT);")
    c.execute("CREATE TABLE earthquakes (earthquake_id INTEGER PRIMARY KEY AUTOINCREMENT, location_name TEXT, latitude REAL, longitude REAL, magnitude REAL, depth REAL, description TEXT, search_time TEXT);")
    db.commit()
    db.close()

def addUser(username, password):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    # datetime formatting for sqlite text
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # omits userID as an input as it autoincrements
    c.execute("INSERT INTO users (username, password, created_at, last_login) VALUES (?, ?, ?, ?)", (username, password, created_at, created_at))
    db.commit()
    db.close()

def updateLoginTime(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    userID = getUserID(username)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE users SET last_login = ? WHERE user_id = ?", (current_time, userID))
    db.commit()
    db.close()

# searches the users DB for the userID associated to the username parameter
def getUserID(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result[0]
    else:
        return -1

def updateUserHistory(username, search_type, current_time):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    userID = getUserID(username)
    c.execute("INSERT INTO userHistory (user_id, search_type, search_time) VALUES (?, ?, ?)", (userID, search_type, current_time))
    db.commit()
    db.close()

def logWeather(username, location_name, latitude, longitude, temperature, humidity, precipitation, wind_speed):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updateUserHistory(username, "weather", current_time)
    c.execute("INSERT INTO weather (location_name, latitude, longitude, temperature, humidity, precipitation, wind_speed, search_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (location_name, latitude, longitude, temperature, humidity, precipitation, wind_speed, current_time))
    db.commit()
    db.close()

def logWeatherHistory(username, location_name, latitude, longitude, year, avg_temperature, avg_precipitation, high_temperature, low_temperature):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updateUserHistory(username, "weatherHistory", current_time)
    c.execute("INSERT INTO weatherHistory (location_name, latitude, longitude, year, avg_temperature, avg_precipitation, high_temperature, low_temperature, search_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (location_name, latitude, longitude, year, avg_temperature, avg_precipitation, high_temperature, low_temperature, current_time))
    db.commit()
    db.close()

def logEarthquakes(username, location_name, latitude, longitude, magnitude, depth, description):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    updateUserHistory(username, "earthquakes", current_time)
    c.execute("INSERT INTO earthquakes (location_name, latitude, longitude, magnitude, depth, description, search_time) VALUES (?, ?, ?, ?, ?, ?, ?)", (location_name, latitude, longitude, magnitude, depth, description, current_time))
    db.commit()
    db.close()

# Database Manipulation

def getTableData(table, valueType, value):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    # make sure that this all exists
    c.execute("SELECT * FROM " + table + " WHERE " + valueType + " = ?", (value,))
    result = c.fetchone()
    db.close()
    # check in case there is an error in fetching data
    if result:
        return result
    else:
        return -1
