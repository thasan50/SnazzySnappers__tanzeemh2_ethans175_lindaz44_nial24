# SnazzySnapeprs - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-??-??
# Time Spent: x hours

import sqlite3
import csv
from datetime import datetime

DB_FILE = "geoTracker.db"

def setup():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE users (userID INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT, created_at TEXT, last_login TEXT);")
    c.execute("CREATE TABLE userHistory (history_id INTEGER PRIMARY KEY AUTOINCREMENT, userID INTEGER, search_type TEXT, location_name TEXT, search_time TEXT);")
    c.execute("CREATE TABLE weather (weather_ID INTEGER PRIMARY KEY AUTOINCREMENT, search_type TEXT, location_name TEXT, latitude REAL, longitude REAL, temperature REAL, humidity INTEGER, precipitation REAL, wind_speed REAL, timestamp TEXT);")
    c.execute("CREATE TABLE history (history_id INTEGER PRIMARY KEY AUTOINCREMENT, search_type TEXT, location_name TEXT, latitude REAL, longitude REAL, year INTEGER, avg_temperature REAL, avg_precipitation REAL, high_temperature REAL, low_temperature REAL);")
    c.execute("CREATE TABLE earthquakes (earthquake_id INTEGER PRIMARY KEY AUTOINCREMENT, search_type TEXT, location_name TEXT, latitude REAL, longitude REAL, magnitude REAL, depth REAL, description TEXT, timestamp TEXT);")
    db.commit()
    db.close()

def addUser(username, password):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("INSERT INTO users (username, password, created_at, last_login) VALUES (?, ?, ?, ?)", (username, password, created_at, created_at))
    db.commit()
    db.close()

def updateLoginTime(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    userID = getUserID(username)
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute("UPDATE users SET last_login = ? WHERE userID = ?", (current_time, userID))
    db.commit()
    db.close()

def getUserID(username):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("SELECT userID FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    db.close()
    if result:
        return result[0]
    else:
        raise ValueError("User not found")

def updateUserHistory(username, search_type, location_name):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    userID = getUserID(username)
    c.execute("INSERT INTO userHistory (userID, search_type, location_name, search_time) VALUES (?, ?, ?, ?)", (userID, search_type, location_name, current_time))
    db.commit()
    db.close()
