# SnazzySnapeprs - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-??-??
# Time Spent: x hours

import sqlite3
import csv

DB_FILE = "geoTracker.db"

def createTables():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE users (userID INTEGER PRIMARY KEY, username TEXT, password TEXT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, last_login DATETIME DEFAULT CURRENT_TIMESTAMP);")
    c.execute("CREATE TABLE userHistory (userID INTEGER PRIMARY KEY, search_type TEXT, location_name TEXT, search_time DATETIME DEFAULT CURRENT_TIMESTAMP);")
    c.execute()
    db.commit()
    db.close()
