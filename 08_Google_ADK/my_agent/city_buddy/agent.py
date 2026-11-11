from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import requests
from dotenv import dotenv_values
from google.adk.agents import Agent
from google.adk.integrations.openai import OpenAIResponsesLlm

# The model name comes from models.env at the repository folder
ROOT = next(p for p in Path(__file__).resolve().parents if (p / "models.env").exists())
MODEL = dotenv_values(ROOT / "models.env")["MODEL_DEFAULT"]


def find_city(city: str) -> dict | None:
    """Look a city up in Open-Meteo: its name, country, coordinates and time zone."""
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        timeout=10,
    )
    locations = geo.json().get("results", [])
    return locations[0] if locations else None


def get_weather(city: str) -> dict:
    """Get the current weather in a city."""
    location = find_city(city)
    if not location:
        return {"status": "error", "message": f"City not found: {city}"}
    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m,apparent_temperature,precipitation,wind_speed_10m",
        },
        timeout=10,
    )
    return {"status": "success", "city": location["name"], **weather.json()["current"]}


def get_local_time(city: str) -> dict:
    """Get the current local time in a city."""
    location = find_city(city)
    if not location:
        return {"status": "error", "message": f"City not found: {city}"}
    now = datetime.now(ZoneInfo(location["timezone"]))
    return {"status": "success", "city": location["name"], "day": now.strftime("%A"), "time": now.strftime("%H:%M")}


root_agent = Agent(
    name="city_buddy",
    model=OpenAIResponsesLlm(model=MODEL),
    description="Tells the current weather and the local time in any city.",
    instruction=(
        "You are a friendly travel buddy. "
        "Use get_weather for current conditions and get_local_time for the time. "
        "Never guess either. Keep answers short."
    ),
    tools=[get_weather, get_local_time],
)
