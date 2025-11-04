from src.weather_notifier import is_rain_expected, get_closest_forecast_hour


def test_is_rain_expected_true():
    assert is_rain_expected("Light rain shower")
    assert is_rain_expected("Heavy RAIN")
    assert not is_rain_expected("Sunny")


def test_get_closest_forecast_hour():
    fake_data = {
        "location": {"localtime": "2025-10-27 10:00"},
        "forecast": {
            "forecastday": [{
                "hour": [
                    {"time": "2025-10-27 10:00", "condition": {"text": "Sunny"}},
                    {"time": "2025-10-27 11:00", "condition": {"text": "Cloudy"}},
                    {"time": "2025-10-27 12:00", "condition": {"text": "Rain"}},
                ]
            }]
        }
    }

    result = get_closest_forecast_hour(fake_data, hours_ahead=2)
    assert result["condition"]["text"] == "Rain"
