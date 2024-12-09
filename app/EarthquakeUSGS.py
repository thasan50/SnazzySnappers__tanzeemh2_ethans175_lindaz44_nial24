# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

from flask import Flask, request, jsonify, render_template
import urllib.parse
import urllib.request
import json

app = Flask(__name__)

USGS_API_URL = "https://earthquake.usgs.gov/fdsnws/event/1/query"
GEOCODING_API_URL = "https://nominatim.openstreetmap.org/search" # NEED TO ADD A CARD FOR THIS

def home():
    return render_template("earthquake_form.html")

def get_earthquake_data_by_place():
    place = request.args.get("place", "New York")
    if not place:
        return jsonify({"error": "Place is required"}), 400

    # Fetch latitude and longitude for the place
    geocode_params = {
        "q": place,
        "format": "json",  # Response format
        "limit": 1         # Only fetch the first result
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

    return jsonify(earthquake_data)

if __name__ == '__main__':
    app.run(debug=True)
