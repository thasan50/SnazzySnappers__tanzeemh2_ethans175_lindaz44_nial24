# SnazzySnappers - Tanzeem Hasan, Ethan Sie, Linda Zhang, Nia Lam
# SoftDev
# P01: ArRESTed Development
# 2024-12-17
# Time Spent: x hours

import json
import urllib.request
from urllib.request import Request, urlopen

def fetch_worldpop_data(country_iso3):
    url = f"https://hub.worldpop.org/rest/data/pop/wpgp?iso3={country_iso3}"
    headers = {"User-Agent": "Mozilla/5.0"} 
    try:
        request = Request(url, headers=headers)
        response = urlopen(request)
        data = json.loads(response.read().decode("utf-8"))
        print(json.dumps(data, indent=4))
    except Exception as e:
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
        response = requests.get(url, params=params)
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
    except requests.exceptions.RequestException as e:
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
        response = requests.get(url, params=params) 
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
    except requests.exceptions.RequestException as e:
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
        response = requests.get(full_url, params=params)
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
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
# fetch_worldpop_data("AUS")  # Replace 'AUS' with the ISO3 code of another country
# fetch_google_fonts() # Don't need a specific thing, prints all fonts
# fetch_openweather_data("London") # Replace London with city of choice
# fetch_visualcrossing_data("New York") # Replace New York with city of choice