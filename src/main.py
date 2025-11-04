# src/main.py
from datetime import datetime, time
import subprocess
import os

from weather_notifier import *
from bart_notifier import *


def notify_mac(message: str):
    """Trigger a macOS Notification using terminal-notifier."""
    subprocess.run([
        "terminal-notifier",
        "-title", "Weather Alert",
        "-message", message
    ])


def main():
    try:
        """Main entrypoint for the weather notification."""
        print(datetime.now().strftime("%Y-%m-%d"))

        # Load API credentials
        url, api_key = load_weather_api_config()

        # Cities to check
        cities = ["San Francisco, CA", "Oakland, CA"]

        for city in cities:
            print(f"\nChecking forecast for {city}...")

            # Fetch and process weather
            data = fetch_weather_data(url=url, api_key=api_key, location=city)
            forecast = get_closest_forecast_hour(data)
            condition = forecast['condition']['text']

            print(f"Forecast: {condition}")

            if is_rain_expected(condition):
                notify_mac(f"Go home, expected rain in {city}")
            else:
                print(f"No rain expected in {city}")

        print("\nDone at:", datetime.now().strftime("%H:%M:%S"))
    except Exception as e:
        notify_mac("weather-notifier Broken!!!")
        print("Error:", e)

    try:
        print("\nChecking Embarcadero Station train status...")
        bart_url, bart_api_key = load_bart_api_config()
        bart_data = fetch_bart_data(bart_url, bart_api_key)

        closest_train = get_closest_bart_train(bart_data)
        if closest_train:
            minutes = closest_train['minutes']
            now_time = datetime.now().time()
            in_time_window = time(16, 45) <= now_time <= time(17, 0)

            if minutes is not None and minutes <= 15 and in_time_window:
                notify_mac(
                    f"BART {closest_train['line']} line train to "
                    f"{closest_train['destination']} arriving in "
                    f"{minutes} minutes."
                )
            else:
                print("No immediate train notifications needed.")
        else:
            print("No upcoming Blue or Green line trains found.")

    except Exception as e:
        notify_mac("BART-notifier Broken!!!")
        print("Error:", e)
    print()


if __name__ == "__main__":
    main()
