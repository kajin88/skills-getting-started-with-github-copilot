"""
Test utilities and helper functions
"""
import random
import string


def generate_test_email(domain="test.com"):
    """Generate a random test email"""
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"{username}@{domain}"


def generate_multiple_test_emails(count=5, domain="test.com"):
    """Generate multiple unique test emails"""
    emails = set()
    while len(emails) < count:
        emails.add(generate_test_email(domain))
    return list(emails)


def get_activity_names():
    """Get list of all activity names for testing"""
    return [
        "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
        "Track and Field", "Art Club", "Drama Club", "Debate Team", "Science Club"
    ]


def get_test_activity_data():
    """Get test activity data structure"""
    return {
        "Test Activity": {
            "description": "A test activity for testing purposes",
            "schedule": "Test schedule",
            "max_participants": 10,
            "participants": ["test1@test.com", "test2@test.com"]
        }
    }


class ActivityTestHelper:
    """Helper class for activity-related testing"""
    
    def __init__(self, client):
        self.client = client
    
    def get_activity_participant_count(self, activity_name):
        """Get current participant count for an activity"""
        response = self.client.get("/activities")
        if response.status_code != 200:
            return None
        
        activities = response.json()
        if activity_name not in activities:
            return None
        
        return len(activities[activity_name]["participants"])
    
    def is_student_registered(self, activity_name, email):
        """Check if a student is registered for an activity"""
        response = self.client.get("/activities")
        if response.status_code != 200:
            return False
        
        activities = response.json()
        if activity_name not in activities:
            return False
        
        return email in activities[activity_name]["participants"]
    
    def signup_student(self, activity_name, email):
        """Helper method to sign up a student"""
        return self.client.post(f"/activities/{activity_name}/signup?email={email}")
    
    def unregister_student(self, activity_name, email):
        """Helper method to unregister a student"""
        return self.client.delete(f"/activities/{activity_name}/unregister?email={email}")
    
    def get_all_activities(self):
        """Get all activities data"""
        response = self.client.get("/activities")
        if response.status_code == 200:
            return response.json()
        return None


def assert_valid_activity_structure(activity_data):
    """Assert that activity data has valid structure"""
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    for field in required_fields:
        assert field in activity_data, f"Missing required field: {field}"
    
    assert isinstance(activity_data["description"], str)
    assert isinstance(activity_data["schedule"], str)
    assert isinstance(activity_data["max_participants"], int)
    assert isinstance(activity_data["participants"], list)
    
    assert activity_data["max_participants"] > 0
    assert len(activity_data["description"]) > 0
    assert len(activity_data["schedule"]) > 0
    
    # All participants should be strings (emails)
    for participant in activity_data["participants"]:
        assert isinstance(participant, str)