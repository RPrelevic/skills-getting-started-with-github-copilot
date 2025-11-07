"""
Test configuration and fixtures for FastAPI tests
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy


@pytest.fixture
def client():
    """FastAPI test client fixture"""
    return TestClient(app)


@pytest.fixture
def sample_activities():
    """Sample activities data for testing"""
    return {
        "Test Activity": {
            "description": "A test activity for testing purposes",
            "schedule": "Test Schedule",
            "max_participants": 5,
            "participants": ["test1@example.com", "test2@example.com"]
        },
        "Empty Activity": {
            "description": "An activity with no participants",
            "schedule": "Empty Schedule",
            "max_participants": 10,
            "participants": []
        }
    }


@pytest.fixture(autouse=True)
def reset_activities(sample_activities):
    """Reset activities data before each test"""
    original_activities = copy.deepcopy(activities)
    activities.clear()
    activities.update(sample_activities)
    yield
    # Restore original activities after test
    activities.clear()
    activities.update(original_activities)