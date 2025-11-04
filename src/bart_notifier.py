# src/bart_notifier.py
from datetime import datetime
from dotenv import load_dotenv
import requests
import os


def load_bart_api_config():
    """Load API URL and key from environment variables."""
    load_dotenv()
    url = os.getenv('BART_API_URL', 'https://api.bart.gov/api/etd.aspx')
    api_key = os.getenv('BART_API_KEY', 'MW9S-E7SL-26DU-VV8V')
    if not url or not api_key:
        raise ValueError(
            "Missing BART_API_URL or BART_API_KEY in environment.")
    return url, api_key


def fetch_bart_data(url: str, api_key: str, station_code: str = "EMBR") -> dict:
    """Fetch real-time BART data for a specific station."""
    params = {
        "cmd": "etd",
        "orig": station_code,
        "key": api_key,
        "json": "y"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def get_closest_bart_train(data: dict, lines=("BLUE", "GREEN")) -> dict:
    """Return the next arriving Blue or Green line train."""
    try:
        station = data["root"]["station"][0]
        etd_list = station["etd"]
    except (KeyError, IndexError):
        return {}

    next_train = None
    next_minutes = float('inf')

    for etd in etd_list:
        for est in etd["estimate"]:
            color = est.get("color")
            minutes = est.get("minutes")
            if color not in lines or minutes in ["Leaving", None]:
                continue
            try:
                m = int(minutes)
            except ValueError:
                continue
            if m < next_minutes:
                next_minutes = m
                next_train = {
                    "destination": etd["destination"],
                    "line": color,
                    "minutes": m,
                    "platform": est.get("platform"),
                    "direction": est.get("direction")
                }

    return next_train or {}
