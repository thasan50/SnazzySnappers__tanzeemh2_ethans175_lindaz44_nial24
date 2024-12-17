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
        plt.stem(x,y,'ro')
    plt.xlabel("3-hour intervals")
    plt.ylabel("Temperature (farenheight)")
    plt.tight_layout()
    plt.savefig('static/goo.png')

def humidity():
    plt.figure()
    a = db.getWeather()
    for row in a:
        x = row[0]
        y = row[5]
        plt.stem(x,y,'bo')
    plt.xlabel("3-hour intervals")
    plt.ylabel("Humidity")
    plt.tight_layout()
    plt.savefig('static/foo.png')

def percipitation():
    plt.figure()
    a = db.getWeather()
    for row in a:
        x = row[0]
        y = row[7]
        plt.stem(x,y,'go')
    plt.xlabel("3-hour intervals")
    plt.ylabel("Percipitations (inches)")
    plt.tight_layout()
    plt.savefig('static/boo.png')