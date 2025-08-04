import requests
import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv("apiKey")
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

def get_forecast(city):
    """Get the 5-day forecast for a city"""
    
    # Build the request URL with the provided city
    url = f"{FORECAST_URL}?q={city}&appid={API_KEY}&units=imperial"
    
    try:
        response = requests.get(url)
        
        # Handle API errors similar to data.py
        if response.status_code == 404:
            raise ValueError(f"City '{city}' not found.")
        elif not response.ok:
            raise RuntimeError(f"API error: {response.status_code} - {response.text}")
        
        data = response.json()
        
        # Process the forecast data
        forecast = {}
        for item in data['list']:
            date = item['dt_txt'].split()[0]
            if date not in forecast:
                forecast[date] = []
            forecast[date].append(item)
        
        # Build daily summary
        daily_forecast = {}
        for date, entries in forecast.items():
            temps = [entry['main']['temp'] for entry in entries]
            weather_info = entries[0]['weather'][0]
            
            daily_forecast[date] = {
                'description': weather_info['description'],
                'icon': weather_info['icon'],
                'high': max(temps),
                'low': min(temps),
                'entries': entries  # Keep full data if needed
            }
        
        return daily_forecast
        
    except requests.RequestException as e:
        raise RuntimeError(f"Network error: {e}")

def get_weather_icon_url(icon_code):
    """Get the URL for a weather icon from OpenWeatherMap"""
    return f"https://openweathermap.org/img/wn/{icon_code}@2x.png"

def get_local_weather_emoji(icon_code):
    """Get a weather emoji based on the icon code (fallback if images don't load)"""
    icon_map = {
        '01d': '☀️',  # clear sky day
        '01n': '🌙',  # clear sky night
        '02d': '⛅',  # few clouds day
        '02n': '☁️',  # few clouds night
        '03d': '☁️',  # scattered clouds
        '03n': '☁️',  # scattered clouds
        '04d': '☁️',  # broken clouds
        '04n': '☁️',  # broken clouds
        '09d': '🌧️',  # shower rain
        '09n': '🌧️',  # shower rain
        '10d': '🌦️',  # rain day
        '10n': '🌧️',  # rain night
        '11d': '⛈️',  # thunderstorm
        '11n': '⛈️',  # thunderstorm
        '13d': '❄️',  # snow
        '13n': '❄️',  # snow
        '50d': '🌫️',  # mist
        '50n': '🌫️',  # mist
    }
    return icon_map.get(icon_code, '🌤️')  # default to partly sunny

def print_forecast(forecast_data):
    """Print a formatted forecast summary"""
    for date, data in forecast_data.items():
        emoji = get_local_weather_emoji(data['icon'])
        print(f"{date}: {emoji} {data['description']}, High: {data['high']:.1f}°F, Low: {data['low']:.1f}°F")