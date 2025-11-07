"""
Tests for data validation and edge cases
"""
import pytest
from fastapi.testclient import TestClient


class TestValidationAndEdgeCases:
    """Test class for validation and edge case scenarios"""

    def test_empty_email_signup(self, client):
        """Test signup with empty email parameter"""
        activity_name = "Test Activity"
        
        # Test with empty email
        response = client.post(f"/activities/{activity_name}/signup?email=")
        # FastAPI should handle this gracefully - empty string is still a valid string
        assert response.status_code == 200

    def test_missing_email_parameter(self, client):
        """Test signup without email parameter"""
        activity_name = "Test Activity"
        
        response = client.post(f"/activities/{activity_name}/signup")
        assert response.status_code == 422  # Validation error
        
        error_data = response.json()
        assert "detail" in error_data
        assert any("email" in str(error).lower() for error in error_data["detail"])

    def test_special_characters_in_activity_name(self, client, sample_activities):
        """Test with special characters in activity name"""
        # Add an activity with special characters to our test data
        from src.app import activities
        special_activity = "Test & Fun Activity!"
        activities[special_activity] = {
            "description": "Activity with special chars",
            "schedule": "Test",
            "max_participants": 5,
            "participants": []
        }
        
        email = "user@example.com"
        
        # URL encode special characters
        import urllib.parse
        encoded_name = urllib.parse.quote(special_activity)
        
        response = client.post(f"/activities/{encoded_name}/signup?email={email}")
        assert response.status_code == 200

    def test_unicode_characters_in_email(self, client):
        """Test with unicode characters in email"""
        activity_name = "Test Activity"
        email = "üser@example.com"  # Unicode character
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
        
        # Verify participant was added correctly
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]

    def test_case_sensitive_activity_names(self, client):
        """Test that activity names are case sensitive"""
        email = "user@example.com"
        
        # Should work with correct case
        response = client.post("/activities/Test Activity/signup?email=" + email)
        assert response.status_code == 200
        
        # Should fail with wrong case
        response = client.post("/activities/test activity/signup?email=" + email)
        assert response.status_code == 404

    def test_long_email_address(self, client):
        """Test with very long email address"""
        activity_name = "Empty Activity"
        long_email = "a" * 100 + "@" + "b" * 100 + ".com"
        
        response = client.post(f"/activities/{activity_name}/signup?email={long_email}")
        assert response.status_code == 200
        
        # Verify it was stored correctly
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert long_email in activities_data[activity_name]["participants"]

    def test_concurrent_signups_same_activity(self, client):
        """Test multiple signups to the same activity"""
        activity_name = "Empty Activity"
        emails = [f"user{i}@example.com" for i in range(10)]
        
        # Sign up multiple users rapidly
        responses = []
        for email in emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            responses.append(response)
        
        # All should succeed
        for response in responses:
            assert response.status_code == 200
        
        # Verify all participants are registered
        activities_response = client.get("/activities")
        data = activities_response.json()
        participants = data[activity_name]["participants"]
        assert len(participants) == 10
        for email in emails:
            assert email in participants

    def test_signup_to_full_activity(self, client, sample_activities):
        """Test signup when activity is at max capacity"""
        # Modify test activity to be nearly full
        from src.app import activities
        activity_name = "Test Activity"
        activities[activity_name]["max_participants"] = 2  # Already has 2 participants
        
        email = "newuser@example.com"
        
        # This should still work (no capacity check in current implementation)
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
        
        # Note: Current implementation doesn't enforce max_participants limit
        # This test documents current behavior

    def test_activities_data_structure(self, client, sample_activities):
        """Test that activities data has correct structure"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        
        for activity_name, activity_data in data.items():
            # Check required fields exist
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            
            # Check data types
            assert isinstance(activity_data["description"], str)
            assert isinstance(activity_data["schedule"], str)
            assert isinstance(activity_data["max_participants"], int)
            assert isinstance(activity_data["participants"], list)
            
            # Check participants are strings (emails)
            for participant in activity_data["participants"]:
                assert isinstance(participant, str)

    def test_http_methods_not_allowed(self, client):
        """Test that only allowed HTTP methods work"""
        # GET should work for /activities
        response = client.get("/activities")
        assert response.status_code == 200
        
        # POST should not work for /activities (only for signup)
        response = client.post("/activities")
        assert response.status_code in [404, 405]  # Method not allowed or not found
        
        # PUT should not work
        response = client.put("/activities")
        assert response.status_code in [404, 405]