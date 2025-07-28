import requests
import datetime

URL = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&appid={API_KEY}&units=imperial"

response = requests.get(URL)
data = response.json()
def get_forecast(city): #get the 5 day6 forecast for a city
    forecast = {}
    for item in data['list']:
        date = item['dt_txt'].split()[0]
        if date not in forecast:
            forecast[date] = []
        forecast[date].append(item)

    # Print daily summary
    for date, entries in forecast.items():
        temps = [entry['main']['temp'] for entry in entries]
        weather = entries[0]['weather'][0]['description']
        print(f"{date}: {weather}, High: {max(temps):.1f}°F, Low: {min(temps):.1f}°F")