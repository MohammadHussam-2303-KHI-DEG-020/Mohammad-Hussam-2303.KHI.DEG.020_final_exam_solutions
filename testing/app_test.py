import json
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import app

@pytest.fixture
def test_client():
    return TestClient(app.app)

def test_get_weather_from_cache(test_client):
    with patch("app._get_redis_client") as redis_mock:
        redis_mock.return_value.exists.return_value = True
        redis_mock.return_value.get.return_value = json.dumps(
            {"temp_min": 10, "temp_max": 20}
        )

        response = test_client.get("/weather/24.86/67.01")

        assert response.status_code == 200
        assert response.json() == {
            "source": "cache",
            "data": {"temp_min": 10, "temp_max": 20},
        }

def test_get_weather_from_api(test_client):
    with patch("app._get_redis_client") as redis_mock, \
         patch("app.requests.get") as requests_mock:
        redis_mock.return_value.exists.return_value = False
        requests_mock.return_value.status_code = 200
        requests_mock.return_value.json.return_value = {
            "daily": {
                "temperature_2m_min": [15, 16, 17],
                "temperature_2m_max": [25, 26, 27],
            }
        }

        response = test_client.get("/weather/24.86/67.01")

        assert response.status_code == 200
        assert response.json() == {
            "source": "API",
            "data": {"temp_min": 15, "temp_max": 27, "latitude": 24.86, "longitude": 67.01},
        }

def test_get_weather_invalid_coordinates(test_client):
    response = test_client.get("/weather/invalid/coordinates")

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["path", "latitude"],
                "msg": "value is not a valid float",
                "type": "type_error.float"
            },
            {
                "loc": ["path", "longitude"],
                "msg": "value is not a valid float",
                "type": "type_error.float"
            }
        ]
    }

def test_get_weather_cache_failure(test_client):
    with patch("app._get_redis_client") as redis_mock:
        redis_mock.return_value.exists.return_value = False
        redis_mock.return_value.get.side_effect = Exception("Redis connection failed")

        response = test_client.get("/weather/24.86/67.01")

        assert response.status_code == 200
        assert response.json() == {
            "source": "API",
            "data": {
                "temp_min": 29.0,
                "temp_max": 34.4,
                "latitude": 24.86,
                "longitude": 67.01
            }
        }
