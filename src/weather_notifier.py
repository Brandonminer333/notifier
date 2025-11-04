from datetime import datetime, timedelta
from dotenv import load_dotenv
import subprocess
import requests
import os


def load_weather_api_config():
    """Load API URL and key from environment variables."""
    load_dotenv()
    url = os.getenv('WEATHERAPI_URL')
    api_key = os.getenv('WEATHERAPI_API_KEY')
    if not url or not api_key:
        raise ValueError(
            "Missing WEATHERAPI_URL or WEATHERAPI_API_KEY in environment.")
    return url, api_key


def fetch_weather_data(url: str, api_key: str, location: str = "San Francisco", days: int = 1) -> dict:
    """Fetch forecast data from WeatherAPI."""
    params = {
        "key": api_key,
        "q": location,
        "days": days,
        "aqi": "no",
        "alerts": "no",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_closest_forecast_hour(data: dict, hours_ahead: int = 1) -> dict:
    """Find the forecast hour closest to now + `hours_ahead`."""
    hours = data["forecast"]["forecastday"][0]["hour"]
    local_time_str = data["location"]["localtime"]
    local_time = datetime.strptime(local_time_str, "%Y-%m-%d %H:%M")
    target_time = local_time + timedelta(hours=hours_ahead)

    closest = min(hours, key=lambda h: abs(
        datetime.strptime(h["time"], "%Y-%m-%d %H:%M") - target_time
    ))
    return closest


def is_rain_expected(condition: str) -> bool:
    """Return True if the condition suggests rain."""
    return "rain" in condition.lower()
