"""
Test cases for FastAPI endpoints
"""
import pytest


class TestRootEndpoint:
    """Test the root endpoint"""
    
    def test_root_redirects_to_static_index(self, client):
        """Test that root endpoint redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestActivitiesEndpoint:
    """Test the activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """Test that GET /activities returns all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities_data = response.json()
        assert isinstance(activities_data, dict)
        assert len(activities_data) == 9  # Expected number of activities
        
        # Check that expected activities are present
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class", "Soccer Team",
            "Track and Field", "Art Club", "Drama Club", "Debate Team", "Science Club"
        ]
        for activity in expected_activities:
            assert activity in activities_data
    
    def test_activities_have_required_fields(self, client, reset_activities):
        """Test that each activity has required fields"""
        response = client.get("/activities")
        activities_data = response.json()
        
        for activity_name, activity_info in activities_data.items():
            assert "description" in activity_info
            assert "schedule" in activity_info
            assert "max_participants" in activity_info
            assert "participants" in activity_info
            assert isinstance(activity_info["participants"], list)
            assert isinstance(activity_info["max_participants"], int)


class TestSignupEndpoint:
    """Test the signup endpoint"""
    
    def test_signup_for_existing_activity_success(self, client, reset_activities):
        """Test successful signup for an existing activity"""
        test_email = "test@mergington.edu"
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["message"] == f"Signed up {test_email} for {activity_name}"
        
        # Verify the student was added to the activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert test_email in activities_data[activity_name]["participants"]
    
    def test_signup_for_nonexistent_activity_fails(self, client, reset_activities):
        """Test that signing up for a non-existent activity fails"""
        test_email = "test@mergington.edu"
        activity_name = "Nonexistent Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_signup_duplicate_email_fails(self, client, reset_activities):
        """Test that signing up with an email already registered fails"""
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email={existing_email}")
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"
    
    def test_signup_different_activity_same_email_success(self, client, reset_activities):
        """Test that the same email can sign up for different activities"""
        test_email = "test@mergington.edu"
        
        # Sign up for first activity
        response1 = client.post(f"/activities/Chess Club/signup?email={test_email}")
        assert response1.status_code == 200
        
        # Sign up for second activity with same email
        response2 = client.post(f"/activities/Programming Class/signup?email={test_email}")
        assert response2.status_code == 200
        
        # Verify the student is in both activities
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert test_email in activities_data["Chess Club"]["participants"]
        assert test_email in activities_data["Programming Class"]["participants"]


class TestUnregisterEndpoint:
    """Test the unregister endpoint"""
    
    def test_unregister_from_activity_success(self, client, reset_activities):
        """Test successful unregistration from an activity"""
        existing_email = "michael@mergington.edu"  # Already in Chess Club
        activity_name = "Chess Club"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={existing_email}")
        assert response.status_code == 200
        
        response_data = response.json()
        assert response_data["message"] == f"Unregistered {existing_email} from {activity_name}"
        
        # Verify the student was removed from the activity
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert existing_email not in activities_data[activity_name]["participants"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client, reset_activities):
        """Test that unregistering from a non-existent activity fails"""
        test_email = "test@mergington.edu"
        activity_name = "Nonexistent Club"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"
    
    def test_unregister_not_registered_email_fails(self, client, reset_activities):
        """Test that unregistering an email not registered for activity fails"""
        test_email = "notregistered@mergington.edu"
        activity_name = "Chess Club"
        
        response = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not registered for this activity"


class TestIntegrationScenarios:
    """Integration tests for complex scenarios"""
    
    def test_signup_and_unregister_workflow(self, client, reset_activities):
        """Test complete signup and unregister workflow"""
        test_email = "workflow@mergington.edu"
        activity_name = "Science Club"
        
        # Initial state - check student is not registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert test_email not in activities_data[activity_name]["participants"]
        
        # Sign up
        signup_response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        assert signup_response.status_code == 200
        
        # Verify signup
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert test_email in activities_data[activity_name]["participants"]
        
        # Unregister
        unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={test_email}")
        assert unregister_response.status_code == 200
        
        # Verify unregistration
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert test_email not in activities_data[activity_name]["participants"]
    
    def test_multiple_students_same_activity(self, client, reset_activities):
        """Test multiple students signing up for the same activity"""
        activity_name = "Art Club"
        test_emails = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]
        
        # Sign up multiple students
        for email in test_emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all students are registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        for email in test_emails:
            assert email in activities_data[activity_name]["participants"]