import pytest
from app.services import StudentService, ValidationError
from app.main import create_app


@pytest.fixture
def svc():
    return StudentService()


def test_add_and_get_student(svc):
    svc.add_student("P001", "Asha", "asha@college.edu")
    assert svc.get_student("P001")["name"] == "Asha"


def test_duplicate_prn_rejected(svc):
    svc.add_student("P001", "Asha", "asha@college.edu")
    with pytest.raises(ValidationError):
        svc.add_student("P001", "Ravi", "ravi@college.edu")


def test_invalid_email_rejected(svc):
    with pytest.raises(ValidationError):
        svc.add_student("P002", "Ravi", "not-an-email")


def test_course_registration_and_duplicate(svc):
    svc.add_student("P001", "Asha", "asha@college.edu")
    svc.add_course("CS101", "Intro to CS")
    assert svc.enroll("P001", "CS101") == ["CS101"]
    with pytest.raises(ValidationError):
        svc.enroll("P001", "CS101")


def test_unknown_student_lookup(svc):
    with pytest.raises(ValidationError):
        svc.get_student("NOPE")


def test_health_endpoint():
    client = create_app().test_client()
    r = client.get("/health")
    assert r.status_code == 200 and r.get_json()["status"] == "UP"
