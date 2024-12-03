# SnazzySnapeprs - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-??-??
# Time Spent: x hours

import sqlite3
import csv

DB_FILE = "geoTracker.db"
latestUID = -1

def createTables():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE users (userID INTEGER PRIMARY KEY, username TEXT, password TEXT, created_at TEXT, last_login TEXT);")
    c.execute("CREATE TABLE userHistory (userID INTEGER PRIMARY KEY, search_type TEXT, location_name TEXT, search_time TEXT);")
    c.execute("CREATE TABLE weather (search_type TEXT, weather_id INTEGER, location_name TEXT, latitude REAL, longitude REAL, temperature REAL, humidity INTEGER, precipitation REAL, wind_speed REAL, timestamp TEXT);")
    c.execute("CREATE TABLE history (search_type TEXT, history_id INTEGER, location_name TEXT, latitude REAL, longitude REAL, year INTEGER, avg_temperature REAL, avg_precipitation REAL, high_temperature REAL, low_temperature REAL);")
    c.execute("CREATE TABLE earthquakes (search_type TEXT, earthquake_id INTEGER, location_name TEXT, latitude REAL, longitude REAL, magnitude REAL, depth REAL, description TEXT, timestamp TEXT);")
    db.commit()
    db.close()

def addUser(username, password):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    global latestUID
    latestUID += 1
    c.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)", latestUID, username, password, {TIME HERE}, {TIME HERE})
    db.commit()
    db.close()

def updateLoginTime(user):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("UPDATE users SET last_login = '{TIME HERE}', WHERE username = user" )
    db.commit()
    db.close()
