# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

from flask import Flask, request, jsonify, render_template
import urllib.parse
import urllib.request
import requests
import json
import db

def fetch_google_fonts():
    with open("keys/key_GoogleFonts.txt", "r") as file:
        api_key = file.read().strip()
    if not api_key:
        raise ValueError("API key file is empty. Please add a valid API key.")
    url = "https://www.googleapis.com/webfonts/v1/webfonts"
    params = {
        "key": api_key
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        fonts_data = response.json()
        print(json.dumps(fonts_data, indent=4))

def fetch_city_pop(city_name):
    with open("keys/key_APINinjaCity.txt", "r") as file:
        api_key = file.read().strip()
    if not api_key:
        raise ValueError("API key file is empty. Please add a valid API key.")

    api_url = f'https://api.api-ninjas.com/v1/city?name={city_name}'
    request = urllib.request.Request(api_url)
    request.add_header('X-Api-Key', api_key)
    try:
        with urllib.request.urlopen(request) as response:
            if response.status == 200:
                print(response.read().decode('utf-8'))
            else:
                print("Error:", response.status, response.reason)
    except urllib.error.URLError as e:
        print("Failed to fetch data:", e)

def fetch_openweather(lat, lon):
    with open("keys/key_OpenWeatherMap.txt", "r") as file:
        api_key = file.read().strip()
    if not api_key:
        raise ValueError("API key file is empty. Please add a valid API key.")
    response = requests.get(f'''http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt=40&units=imperial&appid={api_key}''')
    if response.status_code == 200:
        return response.json()

def possible_city(city_name):
    with open("keys/key_OpenWeatherMap.txt", "r") as file:
        api_key = file.read().strip()
    if not api_key:
        raise ValueError("API key file is empty. Please add a valid API key.")
    with requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=5&appid={api_key}") as response:
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            print(f"Response: {response.text}")

def fetch_visualcrossing_data(location):
    try:
        with open("keys/key_VisualCrossing.txt", "r") as file:
            api_key = file.read().strip()
        if not api_key:
            raise ValueError("API key file is empty. Please add a valid API key.")
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        full_url = f"{url}/{location}"
        params = {
            "key": api_key,
            "unitGroup": "metric"
        }
        response = requests.get(full_url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            print(json.dumps(weather_data, indent=4))
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            print(f"Response: {response.text}")

    except ValueError as ve:
        print(f"Error: {ve}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_earthquake_data(username):
    USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"

    place = request.args.get("place", None)
    year = request.args.get("year", None)
    if not place:
        return {"error": "Place is required"}
    if not year:
        return {"error": "Year is required"}

    # Fetch latitude and longitude for the place
    geocode_params = {
        "q": place,
        "format": "json",
        "limit": 1
    }
    geocode_query = urllib.parse.urlencode(geocode_params)
    geocode_url = f"{GEOCODING_API_URL}?{geocode_query}"

    try:
        with urllib.request.urlopen(geocode_url) as response:
            geocode_data = json.loads(response.read())
            if not geocode_data:
                return {"error": "Place not found"}

            latitude = geocode_data[0]["lat"]
            longitude = geocode_data[0]["lon"]
    except urllib.error.URLError as e:
        return {"error": f"Geocoding failed: {e}"}

    # Fetch earthquake data
    starttime = f"{year}-01-01"
    endtime = f"{year}-12-31"
    earthquake_params = {
        "format": "geojson",
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": 500,
        "starttime": starttime,
        "endtime": endtime,
        "minmagnitude": "4.5",
    }
    earthquake_query = urllib.parse.urlencode(earthquake_params)
    earthquake_url = f"{USGS_API_URL}?{earthquake_query}"

    try:
        with urllib.request.urlopen(earthquake_url) as response:
            earthquake_data = json.loads(response.read())
    except urllib.error.URLError as e:
        return {"error": f"Earthquake API failed: {e}"}

    # Parse earthquake data
    features = earthquake_data.get('features', [])
    if not features:
        return {"error": "No earthquake data found"}

    earthquakes = [
        {
            "place": feature["properties"]["place"],
            "lat": feature["geometry"]["coordinates"][1],
            "lon": feature["geometry"]["coordinates"][0],
            "magnitude": feature["properties"]["mag"],
            "depth": feature["geometry"]["coordinates"][2],
            "description": feature["properties"]["title"],
        }
        for feature in features
    ]
    return earthquakes