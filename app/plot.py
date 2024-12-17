import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import db

def forecast():
    plt.figure()
    a = db.getWeather()
    for row in a:
        x = row[0]
        y = row[4]
        plt.plot(x,y,'ro-')
    plt.xlabel("3-hour intervals")
    plt.ylabel("temperature")
    plt.tight_layout()
    plt.savefig('static/goo.png')

def humidity():
    plt.figure()
    a = db.getWeather()
    for row in a:
        x = row[0]
        y = row[5]
        plt.plot(x,y,'bo-')
    plt.xlabel("3-hour intervals")
    plt.ylabel("humidity")
    plt.tight_layout()
    plt.savefig('static/foo.png')

def percipitation():
    plt.figure()
    a = db.getWeather()
    for row in a:
        x = row[0]
        y = row[7]
        plt.plot(x,y,'go-')
    plt.xlabel("3-hour intervals")
    plt.ylabel("humidity")
    plt.tight_layout()
    plt.savefig('static/boo.png')