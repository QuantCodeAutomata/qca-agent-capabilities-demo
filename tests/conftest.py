"""Pytest configuration and fixtures for API testing."""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.storage import data_store


@pytest.fixture(scope="function")
def client():
    """
    Create a TestClient instance for API testing.
    
    This fixture provides a fresh TestClient for each test function,
    ensuring test isolation.
    
    Yields:
        TestClient: FastAPI test client instance
    """
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function", autouse=True)
def clean_storage():
    """
    Clear data storage before and after each test.
    
    This fixture automatically runs for every test function,
    ensuring a clean state for data persistence tests.
    """
    data_store.clear_all()
    yield
    data_store.clear_all()


@pytest.fixture
def sample_analysis_data():
    """
    Provide sample valid analysis data.
    
    Returns:
        dict: Valid analysis request data
    """
    return {
        "data": {
            "temperature": 23.5,
            "humidity": 60,
            "pressure": 1013.25
        },
        "metadata": {
            "source": "sensor-1",
            "location": "room-A",
            "unit": "celsius"
        }
    }


@pytest.fixture
def sample_analysis_data_no_metadata():
    """
    Provide sample analysis data without metadata.
    
    Returns:
        dict: Valid analysis request data without metadata
    """
    return {
        "data": {
            "value": 42,
            "status": "active"
        }
    }


@pytest.fixture
def multiple_analysis_records():
    """
    Provide multiple sample analysis records.
    
    Returns:
        list: List of valid analysis request data
    """
    return [
        {
            "data": {"temperature": 20.0, "humidity": 55},
            "metadata": {"source": "sensor-1"}
        },
        {
            "data": {"temperature": 22.5, "humidity": 58},
            "metadata": {"source": "sensor-2"}
        },
        {
            "data": {"temperature": 21.0, "humidity": 60},
            "metadata": {"source": "sensor-3"}
        },
        {
            "data": {"temperature": 23.0, "humidity": 57},
            "metadata": {"source": "sensor-4"}
        },
        {
            "data": {"temperature": 19.5, "humidity": 62},
            "metadata": {"source": "sensor-5"}
        }
    ]


@pytest.fixture
def empty_data_payload():
    """
    Provide invalid payload with empty data field.
    
    Returns:
        dict: Invalid request with empty data
    """
    return {
        "data": {},
        "metadata": {"source": "test"}
    }


@pytest.fixture
def nested_data_payload():
    """
    Provide complex nested data structure.
    
    Returns:
        dict: Valid request with nested data
    """
    return {
        "data": {
            "sensor_readings": {
                "temperature": {
                    "value": 23.5,
                    "unit": "celsius",
                    "calibration": {
                        "offset": 0.5,
                        "last_calibrated": "2024-01-01"
                    }
                },
                "humidity": {
                    "value": 60,
                    "unit": "percent"
                }
            },
            "location": {
                "building": "A",
                "floor": 3,
                "room": "301"
            },
            "tags": ["production", "critical", "monitored"]
        },
        "metadata": {
            "version": "2.0",
            "protocol": "mqtt"
        }
    }
