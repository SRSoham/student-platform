import pytest
from app.main import create_app


@pytest.fixture
def client():
    return create_app().test_client()


def test_full_api_flow(client):
    assert client.post("/students", json={"prn": "P001", "name": "Asha", "email": "a@c.edu"}).status_code == 201
    assert client.post("/courses", json={"code": "CS101", "title": "Intro"}).status_code == 201
    assert client.post("/enroll", json={"prn": "P001", "code": "CS101"}).get_json()["courses"] == ["CS101"]
    assert client.post("/marks", json={"prn": "P001", "code": "CS101", "marks": 85}).status_code == 201
    assert client.get("/students/P001/gpa").get_json()["gpa"] == 9.0
    assert len(client.get("/students").get_json()) == 1


def test_api_validation_error_returns_400(client):
    r = client.post("/students", json={"prn": "P001", "name": "Asha", "email": "bad"})
    assert r.status_code == 400
    assert "error" in r.get_json()
