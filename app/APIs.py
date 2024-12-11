# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

from flask import Flask, request, jsonify, render_template
import urllib.parse
import urllib.request
import json
import db

def fetch_city_pop(city_name):
    try:
        with open(key_file_path, "r") as file:
            api_key = file.read().strip()
        if not api_key:
            raise ValueError("API key file is empty. Please add a valid API key.")
        url = "https://api.api-ninjas.com/v1/"
        params = {
            "city": city_name,
            "X-Api-Key": api_key
        }
        response = request.get(url, params = params)
        if response.status_code == 200:
            fonts_data = response.json()
            print(json.dumps(city_data, indent=4))
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            print(f"Response: {response.text}")

    except FileNotFoundError:
        print(f"Error: The file '{key_file_path}' was not found. Please create it and add your API key.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except request.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_google_fonts():
    key_file_path = os.path.join("keys", "key_GoogleFonts.txt")
    try:
        with open(key_file_path, "r") as file:
            api_key = file.read().strip()
        if not api_key:
            raise ValueError("API key file is empty. Please add a valid API key.")
        url = "https://www.googleapis.com/webfonts/v1/webfonts"
        params = {
            "key": api_key
        }
        response = request.get(url, params=params)
        if response.status_code == 200:
            fonts_data = response.json()
            print(json.dumps(fonts_data, indent=4))
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            print(f"Response: {response.text}")

    except FileNotFoundError:
        print(f"Error: The file '{key_file_path}' was not found. Please create it and add your API key.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except request.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_openweather_data(city_name):
    key_file_path = os.path.join("keys", "key_OpenWeather.txt")
    try:
        with open(key_file_path, "r") as file:
            api_key = file.read().strip()
        if not api_key:
            raise ValueError("API key file is empty. Please add a valid API key.")
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city_name,
            "appid": api_key,
            "units": "metric"
        }
        response = request.get(url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            print(json.dumps(weather_data, indent=4))
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            print(f"Response: {response.text}")

    except FileNotFoundError:
        print(f"Error: The file '{key_file_path}' was not found. Please create it and add your API key.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except request.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_visualcrossing_data(location):
    key_file_path = os.path.join("keys", "key_VisualCrossing.txt")
    try:
        with open(key_file_path, "r") as file:
            api_key = file.read().strip()
        if not api_key:
            raise ValueError("API key file is empty. Please add a valid API key.")
        url = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        full_url = f"{url}/{location}"
        params = {
            "key": api_key,
            "unitGroup": "metric"
        }
        response = request.get(full_url, params=params)
        if response.status_code == 200:
            weather_data = response.json()
            print(json.dumps(weather_data, indent=4))
        else:
            print(f"Error: Unable to fetch data (Status code: {response.status_code})")
            print(f"Response: {response.text}")

    except FileNotFoundError:
        print(f"Error: The file '{key_file_path}' was not found. Please create it and add your API key.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except request.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def fetch_earthquake_data(username):
    USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
    GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search"

    place = request.args.get("place", None)
    if not place:
        return jsonify({"error": "Place is required"}), 400

    # Fetch latitude and longitude for the place
    geocode_params = {
        "q": place,
        "format": "json",  # Response format
        "limit": 0         # Only fetch the first result
    }
    geocode_query = urllib.parse.urlencode(geocode_params)
    geocode_url = f"{GEOCODING_API_URL}?{geocode_query}"

    try:
        with urllib.request.urlopen(geocode_url) as response:
            geocode_data = json.loads(response.read())
            if not geocode_data:
                return jsonify({"error": "Place not found"}), 404

            # Extract latitude and longitude
            latitude = geocode_data[0]["lat"]
            longitude = geocode_data[0]["lon"]
    except urllib.error.URLError as e:
        return jsonify({"error": f"Geocoding failed: {e}"}), 500

    # Use the latitude and longitude to fetch earthquake data
    earthquake_params = {
        "format": "geojson",
        "latitude": latitude,
        "longitude": longitude,
        "maxradiuskm": request.args.get("maxradiuskm", "500"),
        "starttime": request.args.get("starttime", "2024-01-01"),
        "endtime": request.args.get("endtime", "2024-12-31"),
        "minmagnitude": request.args.get("minmagnitude", "4.5"),
    }
    earthquake_query = urllib.parse.urlencode(earthquake_params)
    earthquake_url = f"{USGS_API_URL}?{earthquake_query}"

    try:
        with urllib.request.urlopen(earthquake_url) as response:
            earthquake_data = json.loads(response.read())
    except urllib.error.URLError as e:
        return jsonify({"error": f"Earthquake API failed: {e}"}), 500
    features = earthquake_data.get('features')[0]

    db.logEarthquakes(username, place, latitude, longitude, features['properties']['mag'], features['properties']['dmin'], features['properties']['title'])
