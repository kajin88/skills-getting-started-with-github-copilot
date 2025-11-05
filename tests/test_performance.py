"""
Performance and load testing for the API
"""
import pytest
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


class TestPerformance:
    """Test API performance characteristics"""
    
    def test_activities_endpoint_response_time(self, client, reset_activities):
        """Test that activities endpoint responds within reasonable time"""
        start_time = time.time()
        response = client.get("/activities")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_signup_endpoint_response_time(self, client, reset_activities):
        """Test that signup endpoint responds within reasonable time"""
        test_email = "performance@test.com"
        activity_name = "Programming Class"
        
        start_time = time.time()
        response = client.post(f"/activities/{activity_name}/signup?email={test_email}")
        end_time = time.time()
        
        response_time = end_time - start_time
        
        assert response.status_code == 200
        assert response_time < 1.0  # Should respond within 1 second
    
    def test_multiple_sequential_requests(self, client, reset_activities):
        """Test performance with multiple sequential requests"""
        num_requests = 10
        
        start_time = time.time()
        
        for i in range(num_requests):
            response = client.get("/activities")
            assert response.status_code == 200
        
        end_time = time.time()
        total_time = end_time - start_time
        average_time = total_time / num_requests
        
        assert average_time < 0.5  # Each request should take less than 0.5 seconds on average
    
    def test_concurrent_signups_different_activities(self, client, reset_activities):
        """Test concurrent signups to different activities"""
        def signup_to_activity(activity_name, email):
            return client.post(f"/activities/{activity_name}/signup?email={email}")
        
        activities = ["Chess Club", "Programming Class", "Gym Class", "Soccer Team", "Art Club"]
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = []
            for i, activity in enumerate(activities):
                email = f"concurrent{i}@test.com"
                future = executor.submit(signup_to_activity, activity, email)
                futures.append((future, activity, email))
            
            # Wait for all requests to complete
            for future, activity, email in futures:
                response = future.result()
                assert response.status_code == 200
        
        # Verify all signups were successful
        final_response = client.get("/activities")
        activities_data = final_response.json()
        
        for i, activity in enumerate(activities):
            email = f"concurrent{i}@test.com"
            assert email in activities_data[activity]["participants"]


class TestLoadScenarios:
    """Test various load scenarios"""
    
    def test_many_students_same_activity(self, client, reset_activities):
        """Test signing up many students to the same activity"""
        activity_name = "Track and Field"  # Has high max_participants (40)
        num_students = 20
        
        # Sign up multiple students
        for i in range(num_students):
            email = f"student{i}@load-test.com"
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all students are registered
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        
        participants = activities_data[activity_name]["participants"]
        for i in range(num_students):
            email = f"student{i}@load-test.com"
            assert email in participants
    
    def test_rapid_signup_unregister_cycles(self, client, reset_activities):
        """Test rapid signup and unregister cycles"""
        activity_name = "Science Club"
        test_email = "cycle@test.com"
        num_cycles = 10
        
        for cycle in range(num_cycles):
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


class TestStressTest:
    """Stress testing scenarios"""
    
    @pytest.mark.slow
    def test_large_number_of_activities_requests(self, client, reset_activities):
        """Test handling a large number of activities requests"""
        num_requests = 100
        
        responses = []
        start_time = time.time()
        
        for _ in range(num_requests):
            response = client.get("/activities")
            responses.append(response)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # All requests should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Performance should be reasonable
        average_time = total_time / num_requests
        assert average_time < 1.0  # Less than 1 second per request on average
        
        print(f"Completed {num_requests} requests in {total_time:.2f} seconds")
        print(f"Average response time: {average_time:.4f} seconds")
    
    @pytest.mark.slow  
    def test_mixed_operation_stress(self, client, reset_activities):
        """Test mixed operations under stress"""
        num_operations = 50
        
        operations_completed = 0
        start_time = time.time()
        
        for i in range(num_operations):
            email = f"stress{i}@test.com"
            
            # Get activities
            get_response = client.get("/activities")
            assert get_response.status_code == 200
            operations_completed += 1
            
            # Sign up for an activity
            activity_name = "Programming Class"
            signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert signup_response.status_code == 200
            operations_completed += 1
            
            # Get activities again
            get_response2 = client.get("/activities")
            assert get_response2.status_code == 200
            operations_completed += 1
            
            # Unregister from activity
            unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
            assert unregister_response.status_code == 200
            operations_completed += 1
        
        end_time = time.time()
        total_time = end_time - start_time
        
        print(f"Completed {operations_completed} operations in {total_time:.2f} seconds")
        print(f"Average operation time: {total_time/operations_completed:.4f} seconds")