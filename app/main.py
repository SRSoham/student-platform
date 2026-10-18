from flask import Flask, jsonify, request
from app.services import StudentService, MarksService, ValidationError


def create_app():
    app = Flask(__name__)
    students = StudentService()
    marks = MarksService(students)

    @app.errorhandler(ValidationError)
    def handle_validation(err):
        return jsonify(error=str(err)), 400

    @app.get("/health")
    def health():
        return jsonify(status="UP", service="student-platform", version="v1.0.0")

    @app.post("/students")
    def add_student():
        d = request.get_json(force=True)
        return jsonify(students.add_student(d.get("prn"), d.get("name"), d.get("email", ""))), 201

    @app.get("/students")
    def list_students():
        return jsonify(students.list_students())

    @app.post("/courses")
    def add_course():
        d = request.get_json(force=True)
        return jsonify(students.add_course(d.get("code"), d.get("title"))), 201

    @app.post("/enroll")
    def enroll():
        d = request.get_json(force=True)
        return jsonify(courses=students.enroll(d.get("prn"), d.get("code")))

    @app.post("/marks")
    def record_marks():
        d = request.get_json(force=True)
        marks.record_marks(d.get("prn"), d.get("code"), d.get("marks"))
        return jsonify(status="recorded"), 201

    @app.get("/students/<prn>/gpa")
    def gpa(prn):
        return jsonify(prn=prn, gpa=marks.gpa(prn))

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
