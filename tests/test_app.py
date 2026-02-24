import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_unregister():
    # Use a known activity
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@mergington.edu"

    # Ensure not signed up
    client.delete(f"/activities/{activity}/unregister?email={email}")

    # Sign up
    resp_signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_signup.status_code == 200
    assert "Signed up" in resp_signup.json()["message"]

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp_dup.status_code == 400
    assert "already signed up" in resp_dup.json()["detail"]

    # Unregister
    resp_unreg = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg.status_code == 200
    assert "Removed" in resp_unreg.json()["message"]

    # Unregister again should fail
    resp_unreg2 = client.delete(f"/activities/{activity}/unregister?email={email}")
    assert resp_unreg2.status_code == 400
    assert "not signed up" in resp_unreg2.json()["detail"]
