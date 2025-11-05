"""
Test configuration and fixtures for FastAPI tests
"""
import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import the app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities data before each test"""
    # Store original activities
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Team training, drills, and competitive matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["liam@mergington.edu", "noah@mergington.edu"]
        },
        "Track and Field": {
            "description": "Sprint, distance, and field events training",
            "schedule": "Mondays, Wednesdays, Fridays, 4:00 PM - 5:30 PM",
            "max_participants": 40,
            "participants": ["ava@mergington.edu", "mia@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore drawing, painting, and mixed media projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["harper@mergington.edu", "zoe@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stagecraft, and production workshops",
            "schedule": "Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu", "jack@mergington.edu"]
        },
        "Debate Team": {
            "description": "Practice public speaking and competitive debating",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["oliver@mergington.edu", "lucas@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and science fair projects",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 18,
            "participants": ["amelia@mergington.edu", "charlotte@mergington.edu"]
        }
    }
    
    # Reset activities to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Clean up after test
    activities.clear()
    activities.update(original_activities)