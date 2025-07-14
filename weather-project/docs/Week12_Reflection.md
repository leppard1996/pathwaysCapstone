Write a brief paragraph (3–5 sentences) describing:

How you implemented the API call

Any blockers, challenges, or next steps



To implement the API call, I used the requests library in data.py to fetch real-time weather data from OpenWeatherMap API. The function fetch_current_weather(city) builds the request using a city name and a stored API key from my .env file, then parses and returns the JSON response. In the GUI (gui_main.py), the API call is triggered by the "Update" button and displays weather details like temperature, humidity, and conditions. I would like to eventually have a little cartoon weather for each condition like real apps do. I have error handling for if you input a city that does not exist in the database. A challenge I am currently facing was I was trying to fix my file write for the cache, and messed something up so I reset to my old push, and am about to start over. Next steps include integrating historical data fetching, caching results for offline access, and improving error feedback for network or parsing issues.