import json
import os

import redis
import requests
import uvicorn
from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/weather/{latitude}/{longitude}")
def get_weather(latitude: float, longitude: float) -> dict:
    redis_client = _get_redis_client()
    cache_key = f"{latitude:.2f}:{longitude:.2f}"

    # Check if data for this location is stored in the cache.
    if redis_client.exists(cache_key):
        weather_data = redis_client.get(cache_key)
        return {"source": "cache", "data": json.loads(weather_data)}

    # Make a call to the open-meteo API.
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}"
        f"&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    )
    response = requests.get(url, timeout=2.0)
    if response.status_code == 400:
        raise HTTPException(status_code=400, detail=response.json()["reason"])
    response.raise_for_status()
    response_data = response.json()

    # Build response content dict.
    weather_data = _get_min_max_temps(response_data)
    weather_data["latitude"] = latitude
    weather_data["longitude"] = longitude

    SECONDS_IN_24H = 24 * 60 * 60
    redis_client.set(cache_key, json.dumps(weather_data), ex=SECONDS_IN_24H)

    return {"source": "API", "data": weather_data}


def _get_min_max_temps(weather_data: dict) -> dict:
    result_dict = {}
    result_dict["temp_min"] = min(weather_data["daily"]["temperature_2m_min"])
    result_dict["temp_max"] = max(weather_data["daily"]["temperature_2m_max"])
    return result_dict


def _get_redis_client() -> redis.Redis:
    return redis.Redis(host="redis", port=6380, db=0)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=os.getenv("APP_PORT"))
