# Weather Dashboard 🌤️

An easy to use and intuitive weather dashboard built with Python and Tkinter that allows users to check current weather conditions for cities around the world!

## Installation 

### Prerequisites
- Python 3.6 or higher
- Internet connection for API calls

### Setup Steps

1. **Clone or download the project**
   ```bash
   git clone https://github.com/leppard1996/pathwaysCapstone.git
   cd pathwaysCapstone/weather-project
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root directory:
   ```
   apiKey=your_openweather_api_key_here
   weatherAPI=https://api.openweathermap.org/data/2.5/weather
   ```

4. **Get a free API key**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key from the dashboard
   - Add it to your `.env` file (You may have to wait up to an hour for your API key to be valid)

## Usage 🚀

1. **Run the application**
   ```bash
   python main.py
   ```

2. **Using the dashboard**
   - Enter a city name in the input field
   - Select your preferred temperature unit (F or C)
   - Click "Update" to fetch current weather data
   - Click "Clear" to reset to default values

## Project Structure 

```
pathwaysCapstone/
├── data/
│   └── data.py          # Weather API functions and caching
├── docs/
│   └── LICENSE 
|   └── Week11_Reflection.md       
├── gui/
│   └── gui_main.py      # Main GUI application
├── main.py              # Entry point
├── requirements.txt     # Python dependencies
├── LICENSE             # MIT License
├── README.md           # This file
├── .env                # Environment variables (create this)
└── weather_history.txt # Auto-generated cache file
```

## Code Overview

### `data.py`
- **`fetch_current_weather(city)`**: Fetches current weather from OpenWeatherMap API
- **`fetch_history(city, date)`**: Fetches historical weather data
- **`save_to_cache(city, date, data)`**: Saves weather data to local cache
- **`load_from_cache(city, date)`**: Loads cached weather data

### `gui_main.py`
- **`WeatherDashboard`**: Main GUI class
- **`create_widgets()`**: Sets up all GUI elements
- **`update_display()`**: Fetches and displays weather data
- **`temp_unit_update()`**: Handles temperature unit conversion
- **`clear_inputs()`**: Resets the interface

### `main.py`
- Simple entry point that starts the GUI application

## Dependencies 

- **requests**: For making HTTP requests to the weather API
- **python-dotenv**: For loading environment variables from .env file
- **tkinter**: For the GUI (included with Python)

## Error Handling 

The application includes robust error handling for:
- Invalid city names (404 errors)
- API connection issues
- Missing environment variables
- Invalid API responses

## API Information 

This application uses the [OpenWeatherMap API](https://openweathermap.org/api):
- Free tier allows 1000 calls per day
- Current weather data is always fetched in imperial units (Fahrenheit)
- Temperature conversion to Celsius is handled locally

## Future Enhancements 

Potential improvements for future versions:
- 5-day weather forecast
- Weather maps integration
- Weather alerts and notifications

