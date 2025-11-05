"""
Example test using test utilities
"""
import pytest
from .test_utils import ActivityTestHelper, generate_test_email, get_activity_names, assert_valid_activity_structure


class TestWithUtilities:
    """Example tests using test utilities"""
    
    def test_activity_helper_signup_flow(self, client, reset_activities):
        """Test using ActivityTestHelper for signup flow"""
        helper = ActivityTestHelper(client)
        test_email = generate_test_email()
        activity_name = "Chess Club"
        
        # Check initial state
        initial_count = helper.get_activity_participant_count(activity_name)
        assert not helper.is_student_registered(activity_name, test_email)
        
        # Sign up student
        response = helper.signup_student(activity_name, test_email)
        assert response.status_code == 200
        
        # Verify registration
        assert helper.is_student_registered(activity_name, test_email)
        assert helper.get_activity_participant_count(activity_name) == initial_count + 1
    
    def test_all_activities_have_valid_structure(self, client, reset_activities):
        """Test all activities have valid structure using utility function"""
        helper = ActivityTestHelper(client)
        activities = helper.get_all_activities()
        
        assert activities is not None
        assert len(activities) > 0
        
        for activity_name, activity_data in activities.items():
            assert_valid_activity_structure(activity_data)
    
    def test_multiple_random_signups(self, client, reset_activities):
        """Test multiple random signups using utilities"""
        helper = ActivityTestHelper(client)
        activity_names = get_activity_names()
        
        # Test with random activities and emails
        for _ in range(5):
            import random
            activity_name = random.choice(activity_names)
            test_email = generate_test_email()
            
            # Sign up
            response = helper.signup_student(activity_name, test_email)
            assert response.status_code == 200
            
            # Verify registration
            assert helper.is_student_registered(activity_name, test_email)
    
    def test_helper_unregister_flow(self, client, reset_activities):
        """Test unregister flow using helper"""
        helper = ActivityTestHelper(client)
        test_email = generate_test_email()
        activity_name = "Programming Class"
        
        # Sign up first
        signup_response = helper.signup_student(activity_name, test_email)
        assert signup_response.status_code == 200
        assert helper.is_student_registered(activity_name, test_email)
        
        # Get initial count after signup
        count_after_signup = helper.get_activity_participant_count(activity_name)
        
        # Unregister
        unregister_response = helper.unregister_student(activity_name, test_email)
        assert unregister_response.status_code == 200
        
        # Verify unregistration
        assert not helper.is_student_registered(activity_name, test_email)
        assert helper.get_activity_participant_count(activity_name) == count_after_signup - 1