import pytest
from app.services import StudentService, MarksService, ValidationError


@pytest.fixture
def setup():
    s = StudentService()
    s.add_student("P001", "Asha", "asha@college.edu")
    s.add_course("CS101", "Intro to CS")
    s.add_course("MA101", "Maths")
    s.enroll("P001", "CS101")
    s.enroll("P001", "MA101")
    return s, MarksService(s)


def test_grade_point_boundaries():
    assert MarksService.grade_point(95) == 10
    assert MarksService.grade_point(90) == 10
    assert MarksService.grade_point(45) == 5
    assert MarksService.grade_point(30) == 0


def test_gpa_calculation(setup):
    s, m = setup
    m.record_marks("P001", "CS101", 92)   # 10
    m.record_marks("P001", "MA101", 75)   # 8
    assert m.gpa("P001") == 9.0


def test_marks_out_of_range(setup):
    _, m = setup
    with pytest.raises(ValidationError):
        m.record_marks("P001", "CS101", 120)


def test_marks_require_enrollment(setup):
    s, m = setup
    s.add_course("PH101", "Physics")
    with pytest.raises(ValidationError):
        m.record_marks("P001", "PH101", 80)


def test_gpa_without_marks(setup):
    _, m = setup
    with pytest.raises(ValidationError):
        m.gpa("P001")
