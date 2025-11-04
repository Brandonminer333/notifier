from src.bart_notifier import load_bart_api_config, fetch_bart_data
import requests
import os


def test_load_bart_api_config(monkeypatch):
    monkeypatch.setenv("BART_API_URL", "https://api.bart.gov")
    monkeypatch.setenv("BART_API_KEY", "test_api_key")
    url, api_key = load_bart_api_config()
    assert url == "https://api.bart.gov"
    assert api_key == "test_api_key"


def test_fetch_bart_data(monkeypatch):
    class MockResponse:
        @staticmethod
        def json():
            return {"root": {"station": []}}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)
    url = "https://api.bart.gov/api/stn.aspx"
    api_key = "test_api_key"
    data = fetch_bart_data(url, api_key)
    assert "root" in data
    assert "station" in data["root"]
