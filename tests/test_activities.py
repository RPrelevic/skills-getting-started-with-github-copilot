"""
Tests for the activities API endpoints
"""
import pytest
from fastapi.testclient import TestClient


class TestActivitiesAPI:
    """Test class for activities API endpoints"""

    def test_root_redirect(self, client):
        """Test that root redirects to static/index.html"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_get_activities(self, client, sample_activities):
        """Test GET /activities endpoint"""
        response = client.get("/activities")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) == 2
        assert "Test Activity" in data
        assert "Empty Activity" in data
        
        # Check structure of activity data
        test_activity = data["Test Activity"]
        assert test_activity["description"] == "A test activity for testing purposes"
        assert test_activity["schedule"] == "Test Schedule"
        assert test_activity["max_participants"] == 5
        assert len(test_activity["participants"]) == 2
        assert "test1@example.com" in test_activity["participants"]
        assert "test2@example.com" in test_activity["participants"]

    def test_signup_for_activity_success(self, client):
        """Test successful signup for an activity"""
        email = "newuser@example.com"
        activity_name = "Test Activity"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == f"Signed up {email} for {activity_name}"
        
        # Verify participant was added
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]

    def test_signup_activity_not_found(self, client):
        """Test signup for non-existent activity"""
        email = "user@example.com"
        activity_name = "Non-existent Activity"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_signup_already_registered(self, client):
        """Test signup when user is already registered"""
        email = "test1@example.com"  # Already in Test Activity
        activity_name = "Test Activity"
        
        response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert response.status_code == 400
        assert response.json()["detail"] == "Student already signed up for this activity"

    def test_signup_with_url_encoding(self, client):
        """Test signup with URL-encoded activity name and email"""
        email = "user+test@example.com"
        activity_name = "Test Activity"
        
        # URL encode the email
        import urllib.parse
        encoded_email = urllib.parse.quote(email)
        encoded_activity = urllib.parse.quote(activity_name)
        
        response = client.post(f"/activities/{encoded_activity}/signup?email={encoded_email}")
        assert response.status_code == 200
        
        # Verify participant was added with original email
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email in activities_data[activity_name]["participants"]

    def test_unregister_participant_success(self, client):
        """Test successful participant removal"""
        email = "test1@example.com"
        activity_name = "Test Activity"
        
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert response.status_code == 200
        
        data = response.json()
        assert data["message"] == f"Unregistered {email} from {activity_name}"
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]
        assert len(activities_data[activity_name]["participants"]) == 1

    def test_unregister_activity_not_found(self, client):
        """Test unregister from non-existent activity"""
        email = "user@example.com"
        activity_name = "Non-existent Activity"
        
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert response.status_code == 404
        assert response.json()["detail"] == "Activity not found"

    def test_unregister_participant_not_registered(self, client):
        """Test unregister when participant is not registered"""
        email = "notregistered@example.com"
        activity_name = "Test Activity"
        
        response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert response.status_code == 400
        assert response.json()["detail"] == "Student is not signed up for this activity"

    def test_unregister_with_url_encoding(self, client):
        """Test unregister with URL-encoded activity name and email"""
        email = "test1@example.com"
        activity_name = "Test Activity"
        
        # URL encode
        import urllib.parse
        encoded_email = urllib.parse.quote(email)
        encoded_activity = urllib.parse.quote(activity_name)
        
        response = client.delete(f"/activities/{encoded_activity}/participants/{encoded_email}")
        assert response.status_code == 200
        
        # Verify participant was removed
        activities_response = client.get("/activities")
        activities_data = activities_response.json()
        assert email not in activities_data[activity_name]["participants"]

    def test_full_signup_unregister_flow(self, client):
        """Test complete flow: signup then unregister"""
        email = "flowtest@example.com"
        activity_name = "Empty Activity"
        
        # Initial state - no participants
        activities_response = client.get("/activities")
        initial_data = activities_response.json()
        assert len(initial_data[activity_name]["participants"]) == 0
        
        # Signup
        signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
        assert signup_response.status_code == 200
        
        # Verify signup
        activities_response = client.get("/activities")
        after_signup_data = activities_response.json()
        assert email in after_signup_data[activity_name]["participants"]
        assert len(after_signup_data[activity_name]["participants"]) == 1
        
        # Unregister
        unregister_response = client.delete(f"/activities/{activity_name}/participants/{email}")
        assert unregister_response.status_code == 200
        
        # Verify unregister
        activities_response = client.get("/activities")
        final_data = activities_response.json()
        assert email not in final_data[activity_name]["participants"]
        assert len(final_data[activity_name]["participants"]) == 0

    def test_multiple_participants_management(self, client):
        """Test managing multiple participants in the same activity"""
        activity_name = "Empty Activity"
        emails = ["user1@example.com", "user2@example.com", "user3@example.com"]
        
        # Sign up multiple users
        for email in emails:
            response = client.post(f"/activities/{activity_name}/signup?email={email}")
            assert response.status_code == 200
        
        # Verify all are registered
        activities_response = client.get("/activities")
        data = activities_response.json()
        participants = data[activity_name]["participants"]
        assert len(participants) == 3
        for email in emails:
            assert email in participants
        
        # Remove middle participant
        response = client.delete(f"/activities/{activity_name}/participants/{emails[1]}")
        assert response.status_code == 200
        
        # Verify correct participant was removed
        activities_response = client.get("/activities")
        data = activities_response.json()
        participants = data[activity_name]["participants"]
        assert len(participants) == 2
        assert emails[0] in participants
        assert emails[1] not in participants
        assert emails[2] in participants