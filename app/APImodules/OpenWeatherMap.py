# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

import urllib.request, json
from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
def get_worldPop(year, country="US"):
    file = open('../keys/key_WorldPop.txt', 'r')
    content = file.read()
    file.close()
    if content == "":
        return 404
    url = f"https://hub.worldpop.org/rest/data/pop/wpgp?iso3={country}"
    API = urllib.request.urlopen(url)
    data = json.loads(API.read())
    content = []
    for l in data['data_file']:
        content.append(data['datafile'])
    print(content)

if __name__ == "__main__":  # true if this file NOT imported
    app.debug = True        # enable auto-reload upon code change
    app.run()
