"""Business logic for the Student Record & Academic Management Platform."""


class ValidationError(Exception):
    pass


class StudentService:
    def __init__(self):
        self._students = {}   # prn -> dict
        self._courses = {}    # course_code -> title
        self._enrollments = {}  # prn -> set(course_code)

    def add_student(self, prn, name, email):
        if not prn or not name:
            raise ValidationError("PRN and name are required")
        if "@" not in email:
            raise ValidationError("Invalid email address")
        if prn in self._students:
            raise ValidationError("Duplicate PRN")
        self._students[prn] = {"prn": prn, "name": name, "email": email}
        self._enrollments[prn] = set()
        return self._students[prn]

    def get_student(self, prn):
        if prn not in self._students:
            raise ValidationError("Student not found")
        return self._students[prn]

    def list_students(self):
        return list(self._students.values())

    def add_course(self, code, title):
        if not code or not title:
            raise ValidationError("Course code and title are required")
        if code in self._courses:
            raise ValidationError("Duplicate course code")
        self._courses[code] = title
        return {"code": code, "title": title}

    def enroll(self, prn, code):
        self.get_student(prn)
        if code not in self._courses:
            raise ValidationError("Course not found")
        if code in self._enrollments[prn]:
            raise ValidationError("Already enrolled")
        self._enrollments[prn].add(code)
        return sorted(self._enrollments[prn])


class MarksService:
    GRADE_POINTS = [(90, 10), (80, 9), (70, 8), (60, 7), (50, 6), (40, 5)]

    def __init__(self, students):
        self.students = students
        self._marks = {}  # (prn, code) -> marks

    def record_marks(self, prn, code, marks):
        self.students.get_student(prn)
        if code not in self.students._enrollments[prn]:
            raise ValidationError("Student not enrolled in course")
        if not 0 <= marks <= 100:
            raise ValidationError("Marks must be between 0 and 100")
        self._marks[(prn, code)] = marks

    @classmethod
    def grade_point(cls, marks):
        for cutoff, gp in cls.GRADE_POINTS:
            if marks >= cutoff:
                return gp
        return 0

    def gpa(self, prn):
        scores = [m for (p, _), m in self._marks.items() if p == prn]
        if not scores:
            raise ValidationError("No marks recorded")
        return round(sum(self.grade_point(m) for m in scores) / len(scores), 2)
