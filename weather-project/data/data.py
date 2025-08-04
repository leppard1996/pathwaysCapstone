import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY = os.getenv("apiKey")
BASE_URL = os.getenv("weatherAPI")
FORECAST_URL = os.getenv("forecastAPI")

historyFile = os.path.join(os.path.dirname(__file__), "weather_history.txt") #use path to update weather_history.txt later


def fetch_current_weather(city):
    # print(f"Fetching current weather for {city}...")  # Debug statement
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial"  # Always fetch in Fahrenheit
    }
    print(f"Request parameters: {params}")  # Debug statement
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 404:
        raise ValueError(f"City '{city}' not found.") #if the city is not found, raise an error
    elif not response.ok:
        raise RuntimeError(f"API error: {response.status_code} - {response.text}")

    return response.json()

def fetch_history(city): #fetch weather data for a specific date
    url = f"{BASE_URL}/history.json?key={API_KEY}&q={city}"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def save_to_cache(city, date, data):
    """Save a single day's weather data to the cache file."""
    entry = {
        "city": city,
        "date": date,
        "data": data
    }

    with open(historyFile, "a") as f:
        f.write(json.dumps(entry) + "\n")


def load_from_cache(city, date):
    """Load weather data for a specific city and date from cache, if available."""
    if not os.path.exists(historyFile):
        return None

    with open(historyFile, "r") as f:
        for line in f:
            try:
                entry = json.loads(line)
                if entry["city"] == city and entry["date"] == date:
                    return entry["data"]
            except json.JSONDecodeError:
                continue

    return None
