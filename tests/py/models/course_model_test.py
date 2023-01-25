from nebula import db
from nebula.models.course import Course
from nebula.models.course_level import CourseLevel


def test_course_model_creation(empty_app):
    with empty_app.app_context():
        course_level = CourseLevel(
            name="Undergraduate", study_type="Bachelor", code="UG"
        )
        db.session.add(course_level)
        db.session.commit()
        course = Course(name="Math 101", code="MATH101", course_level=course_level)
        db.session.add(course)
        db.session.commit()
        assert course.uuid is not None
        assert course.name == "Math 101"
        assert course.code == "MATH101"
        assert course.course_level.name == "Undergraduate"


def test_course_model_query(empty_app):
    with empty_app.app_context():
        course_level = CourseLevel(
            name="Undergraduate", study_type="Bachelor", code="UG"
        )
        db.session.add(course_level)
        db.session.commit()
        course = Course(name="Math 101", code="MATH101", course_level=course_level)
        db.session.add(course)
        db.session.commit()
        queried_course = Course.query.filter_by(code="MATH101").first()
        assert queried_course is not None
        assert queried_course.name == "Math 101"
        assert queried_course.code == "MATH101"
        assert queried_course.course_level.name == "Undergraduate"


def test_course_model_expose(empty_app):
    with empty_app.app_context():
        course_level = CourseLevel(
            name="Undergraduate", study_type="Bachelor", code="UG"
        )
        db.session.add(course_level)
        db.session.commit()
        course = Course(
            name="Math 101",
            code="MATH101",
            course_level=course_level,
            description="Introduction to Math",
        )
        db.session.add(course)
        db.session.commit()
        exposed_data = course.expose()
        assert exposed_data["id"] == course.uuid
        assert exposed_data["name"] == "Math 101"
        assert exposed_data["code"] == "MATH101"
        assert exposed_data["course_level"]["name"] == "Undergraduate"
        assert exposed_data["description"] == "Introduction to Math"
