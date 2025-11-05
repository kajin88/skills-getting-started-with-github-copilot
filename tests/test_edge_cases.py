"""
Test edge cases and error scenarios
"""
import pytest


class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_signup_with_empty_email(self, client, reset_activities):
        """Test signup with empty email parameter"""
        activity_name = "Chess Club"
        
        response = client.post(f"/activities/{activity_name}/signup?email=")
        # Should still work as empty string is a valid email parameter
        assert response.status_code == 200
        
        # Verify empty email was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert "" in activities_data[activity_name]["participants"]
    
    def test_signup_with_special_characters_in_activity_name(self, client, reset_activities):
        """Test signup with URL-encoded special characters in activity name"""
        # Test with spaces (should work as "Chess Club" exists)
        response = client.post("/activities/Chess%20Club/signup?email=test@test.com")
        assert response.status_code == 200
    
    def test_activities_endpoint_returns_consistent_data_structure(self, client, reset_activities):
        """Test that activities endpoint always returns consistent structure"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        activities_data = response.json()
        
        # Verify each activity has the same structure
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_name, str)
            assert len(activity_name) > 0
            
            required_keys = ["description", "schedule", "max_participants", "participants"]
            for key in required_keys:
                assert key in activity_info, f"Missing key '{key}' in activity '{activity_name}'"
            
            # Type validation
            assert isinstance(activity_info["description"], str)
            assert isinstance(activity_info["schedule"], str)
            assert isinstance(activity_info["max_participants"], int)
            assert isinstance(activity_info["participants"], list)
            
            # Value validation
            assert activity_info["max_participants"] > 0
            assert len(activity_info["description"]) > 0
            assert len(activity_info["schedule"]) > 0
    
    def test_case_sensitive_activity_names(self, client, reset_activities):
        """Test that activity names are case sensitive"""
        # Try with different casing
        response1 = client.post("/activities/chess%20club/signup?email=test@test.com")
        assert response1.status_code == 404  # Should fail - case sensitive
        
        response2 = client.post("/activities/CHESS%20CLUB/signup?email=test@test.com")
        assert response2.status_code == 404  # Should fail - case sensitive
        
        response3 = client.post("/activities/Chess%20Club/signup?email=test@test.com")
        assert response3.status_code == 200  # Should work - exact match


class TestDataIntegrity:
    """Test data integrity and state management"""
    
    def test_participant_count_accuracy(self, client, reset_activities):
        """Test that participant counts are accurate after operations"""
        activity_name = "Drama Club"
        
        # Get initial count
        initial_response = client.get("/activities")
        initial_data = initial_response.json()
        initial_count = len(initial_data[activity_name]["participants"])
        
        # Add a participant
        signup_response = client.post(f"/activities/{activity_name}/signup?email=newstudent@test.com")
        assert signup_response.status_code == 200
        
        # Verify count increased
        after_signup_response = client.get("/activities")
        after_signup_data = after_signup_response.json()
        after_signup_count = len(after_signup_data[activity_name]["participants"])
        assert after_signup_count == initial_count + 1
        
        # Remove the participant
        unregister_response = client.delete(f"/activities/{activity_name}/unregister?email=newstudent@test.com")
        assert unregister_response.status_code == 200
        
        # Verify count returned to original
        final_response = client.get("/activities")
        final_data = final_response.json()
        final_count = len(final_data[activity_name]["participants"])
        assert final_count == initial_count
    
    def test_data_persistence_across_requests(self, client, reset_activities):
        """Test that data changes persist across multiple requests"""
        test_email = "persistence@test.com"
        activity_name = "Science Club"
        
        # Sign up
        client.post(f"/activities/{activity_name}/signup?email={test_email}")
        
        # Multiple requests should show the student is still registered
        for _ in range(3):
            response = client.get("/activities")
            activities_data = response.json()
            assert test_email in activities_data[activity_name]["participants"]
    
    def test_isolated_activity_modifications(self, client, reset_activities):
        """Test that modifications to one activity don't affect others"""
        test_email = "isolation@test.com"
        target_activity = "Art Club"
        other_activity = "Debate Team"
        
        # Get initial state of other activity
        initial_response = client.get("/activities")
        initial_other_participants = initial_response.json()[other_activity]["participants"].copy()
        
        # Modify target activity
        client.post(f"/activities/{target_activity}/signup?email={test_email}")
        
        # Verify other activity is unchanged
        final_response = client.get("/activities")
        final_other_participants = final_response.json()[other_activity]["participants"]
        assert final_other_participants == initial_other_participants


class TestResponseFormat:
    """Test API response formats and content"""
    
    def test_success_response_format(self, client, reset_activities):
        """Test that success responses have correct format"""
        test_email = "format@test.com"
        activity_name = "Track and Field"
        
        response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        assert response.status_code == 200
        
        response_data = response.json()
        assert "message" in response_data
        assert isinstance(response_data["message"], str)
        assert test_email in response_data["message"]
        assert activity_name in response_data["message"]
    
    def test_error_response_format(self, client, reset_activities):
        """Test that error responses have correct format"""
        response = client.post("/activities/NonExistent/signup?email=test@test.com")
        assert response.status_code == 404
        
        response_data = response.json()
        assert "detail" in response_data
        assert isinstance(response_data["detail"], str)
        assert response_data["detail"] == "Activity not found"
    
    def test_activities_response_content_type(self, client, reset_activities):
        """Test that activities endpoint returns proper content type"""
        response = client.get("/activities")
        assert response.status_code == 200
        assert "application/json" in response.headers.get("content-type", "")