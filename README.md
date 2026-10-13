# Climate & Weather Dashboard (Python)

A responsive Flask web app that retrieves live weather and a 5-day forecast using the OpenWeatherMap API.

## Features
- Search weather by city name
- Current temperature and feels-like temperature
- Weather condition, humidity, wind speed, pressure and visibility
- Sunrise and sunset times
- 5-day forecast with weather icons
- Friendly error messages for invalid city, API key, or connection problems
- Responsive dashboard UI

## Tech stack
- Python 3.10+
- Flask
- Requests
- OpenWeatherMap Current Weather and 5 Day / 3 Hour Forecast APIs
- HTML and CSS

## Setup

1. Install Python 3.10 or newer.
2. Create and activate a virtual environment:

   **Windows**
   ```powershell
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

   **macOS/Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Get an API key from https://openweathermap.org/api.
5. Copy `.env.example` to `.env` and add your API key:
   ```env
   OPENWEATHER_API_KEY=your_actual_api_key
   ```
   Keep `.env` private; do not commit it to GitHub.

6. Start the app:
   ```bash
   python app.py
   ```

7. Open http://127.0.0.1:5000 in your browser.

## API endpoints used
- Current weather: `https://api.openweathermap.org/data/2.5/weather`
- 5-day forecast: `https://api.openweathermap.org/data/2.5/forecast`

Temperature is requested in metric units (Celsius). Wind speed is converted from m/s to km/h.

## Important distinction: weather vs. climate
This starter project reports **weather** (current and short-term conditions). Climate analysis requires long-term historical observations, typically over decades. For a CV, describe it as a "Weather Dashboard with Forecasting" unless you add a historical climate dataset and trend analysis.

## Troubleshooting
- `401`: confirm your key is correct and activated. New API keys may take time to become active.
- `404`: check the city name.
- No data: check internet access and the API plan/endpoint access.
