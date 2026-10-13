import os
from datetime import datetime
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()
CURRENT_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"


def fetch_weather(city):
    if not API_KEY:
        raise RuntimeError("Missing API key. Add OPENWEATHER_API_KEY to your .env file.")

    
    params = {
    "q": f"{city},IN",
    "appid": API_KEY,
    "units": "metric"
}
    current_response = requests.get(CURRENT_URL, params=params, timeout=12)
    if current_response.status_code == 404:
        raise ValueError("City not found. Check the spelling and try again.")
    current_response.raise_for_status()
    current = current_response.json()

    forecast_response = requests.get(FORECAST_URL, params=params, timeout=12)
    forecast_response.raise_for_status()
    forecast_data = forecast_response.json()

    forecast = []
    seen_dates = set()
    for item in forecast_data.get("list", []):
        dt = datetime.fromtimestamp(item["dt"])
        day = dt.strftime("%a, %d %b")
        # Use one forecast per date, close to midday when available.
        if day not in seen_dates and 10 <= dt.hour <= 15:
            forecast.append({
                "day": day,
                "temp": round(item["main"]["temp"]),
                "description": item["weather"][0]["description"].title(),
                "icon": item["weather"][0]["icon"],
                "humidity": item["main"]["humidity"],
                "wind": round(item["wind"]["speed"] * 3.6, 1),
            })
            seen_dates.add(day)
        if len(forecast) == 5:
            break

    # Fill any missing dates using the first available forecast entry for that date.
    for item in forecast_data.get("list", []):
        dt = datetime.fromtimestamp(item["dt"])
        day = dt.strftime("%a, %d %b")
        if day not in seen_dates and len(forecast) < 5:
            forecast.append({
                "day": day,
                "temp": round(item["main"]["temp"]),
                "description": item["weather"][0]["description"].title(),
                "icon": item["weather"][0]["icon"],
                "humidity": item["main"]["humidity"],
                "wind": round(item["wind"]["speed"] * 3.6, 1),
            })
            seen_dates.add(day)

    return {
        "city": current["name"],
        "country": current["sys"].get("country", ""),
        "temp": round(current["main"]["temp"]),
        "feels_like": round(current["main"]["feels_like"]),
        "description": current["weather"][0]["description"].title(),
        "icon": current["weather"][0]["icon"],
        "humidity": current["main"]["humidity"],
        "wind": round(current["wind"]["speed"] * 3.6, 1),
        "pressure": current["main"]["pressure"],
        "visibility": round(current.get("visibility", 0) / 1000, 1),
        "sunrise": datetime.fromtimestamp(current["sys"]["sunrise"]).strftime("%I:%M %p"),
        "sunset": datetime.fromtimestamp(current["sys"]["sunset"]).strftime("%I:%M %p"),
        "updated": datetime.now().strftime("%d %b %Y, %I:%M %p"),
        "forecast": forecast,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    city = "Pune"
    if request.method == "POST":
        city = request.form.get("city", "").strip() or "Pune"
    else:
        city = request.args.get("city", "Pune").strip() or "Pune"

    weather = None
    error = None
    try:
        weather = fetch_weather(city)
    except ValueError as exc:
        error = str(exc)
    except requests.exceptions.Timeout:
        error = "The weather service took too long to respond. Please try again."
    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        if status == 401:
            error = "The API key was rejected. Check your OpenWeatherMap API key."
        else:
            error = "Weather data is temporarily unavailable. Please try again later."
    except requests.exceptions.RequestException:
        error = "Could not connect to the weather service. Check your internet connection."
    except RuntimeError as exc:
        error = str(exc)

    return render_template("index.html", weather=weather, error=error, searched_city=city)


if __name__ == "__main__":
    app.run(debug=True)
