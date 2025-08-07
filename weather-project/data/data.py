import requests
import json
import os
import csv
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
    print(f"Req parameters: {params}")
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 404:
        raise ValueError(f"City '{city}' not found.") # If the city is not found, raise an error
    elif not response.ok:
        raise RuntimeError(f"API error: {response.status_code} - {response.text}")

    return response.json()

def export_history_to_csv(csv_filename=None, temp_unit="F"):
    """Export all weather history data to a CSV file."""
    if csv_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"weather_history_{timestamp}.csv"
    
    if not os.path.exists(historyFile):
        print("No history file found. Nothing to export.")
        return
    
    # Define CSV headers - only the fields you need
    headers = ['name', 'date', 'temp', 'humidity', 'precip', 'condition']
    
    csv_path = os.path.join(os.path.dirname(__file__), csv_filename)
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        # Read and process each line from history file
        with open(historyFile, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    date = entry.get('date', '')
                    data = entry.get('data', {})
                    
                    # Extract only the specific data we need
                    temp = data['main']['temp']
                    if temp_unit == "C":
                        temp = (temp - 32) * 5 / 9
                    humidity = data['main']['humidity']
                    precip = data.get('rain', {}).get('1h', 0)
                    condition = data['weather'][0]['description'].title()
                    name = data['name']
                    
                    row = [name, date, temp, humidity, precip, condition]
                    writer.writerow(row)
                    
                except json.JSONDecodeError:
                    print(f"Skipping invalid JSON line: {line.strip()}")
                    continue
                except (KeyError, IndexError) as e:
                    print(f"Missing required data in entry: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line: {e}")
                    continue
    
    print(f"Weather history exported to: {csv_path}")
    return csv_path


def export_filtered_history_to_csv(city_filter=None, date_filter=None, csv_filename=None, temp_unit="F"):
    """Export filtered weather history data to a CSV file.
    
    Args:
        city_filter (str): Filter by city name (case-insensitive)
        date_filter (str): Filter by date (YYYY-MM-DD format)
        csv_filename (str): Custom filename for the CSV file
        temp_unit (str): Temperature unit "F" for Fahrenheit or "C" for Celsius
    """
    if csv_filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filters = []
        if city_filter:
            filters.append(f"city_{city_filter}")
        if date_filter:
            filters.append(f"date_{date_filter}")
        filter_str = "_".join(filters) if filters else "filtered"
        csv_filename = f"weather_history_{filter_str}_{timestamp}.csv"
    
    if not os.path.exists(historyFile):
        print("No history file found. Nothing to export.")
        return
    
    # Define CSV headers - only the fields you need
    headers = ['name', 'date', 'temp', 'humidity', 'precip', 'condition']
    
    csv_path = os.path.join(os.path.dirname(__file__), csv_filename)
    rows_exported = 0
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        
        # Read and process each line from history file
        with open(historyFile, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    city = entry.get('city', '')
                    date = entry.get('date', '')
                    data = entry.get('data', {})
                    
                    # Apply filters
                    if city_filter and city_filter.lower() not in city.lower():
                        continue
                    if date_filter and date != date_filter:
                        continue
                    
                    # Extract only the specific data you need
                    temp = data['main']['temp']
                    if temp_unit == "C":
                        temp = (temp - 32) * 5 / 9
                    humidity = data['main']['humidity']
                    precip = data.get('rain', {}).get('1h', 0)
                    condition = data['weather'][0]['description'].title()
                    name = data['name']
                    
                    row = [name, date, temp, humidity, precip, condition]
                    writer.writerow(row)
                    rows_exported += 1
                    
                except json.JSONDecodeError:
                    continue
                except (KeyError, IndexError) as e:
                    print(f"Missing required data in entry: {e}")
                    continue
                except Exception as e:
                    print(f"Error processing line: {e}")
                    continue
    
    print(f"Exported {rows_exported} records to: {csv_path}")
    return csv_path


def get_search_history_summary():
    """Get a summary of the search history."""
    if not os.path.exists(historyFile):
        print("No history file found.")
        return
    
    cities = set()
    dates = set()
    total_entries = 0
    
    with open(historyFile, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                cities.add(entry.get('city', ''))
                dates.add(entry.get('date', ''))
                total_entries += 1
            except json.JSONDecodeError:
                continue


def get_search_history_summary():
    """Get a summary of the search history."""
    if not os.path.exists(historyFile):
        print("No history file found.")
        return
    
    cities = set()
    dates = set()
    total_entries = 0
    
    with open(historyFile, 'r') as f:
        for line in f:
            try:
                entry = json.loads(line)
                cities.add(entry.get('city', ''))
                dates.add(entry.get('date', ''))
                total_entries += 1
            except json.JSONDecodeError:
                continue
    

if __name__ == "__main__":
    # Print summary of search history
    get_search_history_summary()
