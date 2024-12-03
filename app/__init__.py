# SnazzySnapeprs - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-??-??
# Time Spent: x hours

import random, db
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def hello_world():
    return ""

if __name__ == "__main__":
    app.debug = True
    app.run()
