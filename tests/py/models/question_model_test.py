import pytest

from nebula import db
from nebula.models.course import Course
from nebula.models.course_level import CourseLevel
from nebula.models.question import Question
from nebula.models.subject_tag import SubjectTag
from nebula.models.user import User


def test_question_model_creation(empty_app):
    with empty_app.app_context():
        user = User(
            username="test_user", email="test@example.com", password="password123"
        )
        db.session.add(user)
        course_level = CourseLevel(
            name="Undergraduate", code="UGRD", study_type="Bachelor"
        )
        db.session.add(course_level)
        course = Course(name="Math 101", code="MATH101", course_level=course_level)
        db.session.add(course)
        subject_tag = SubjectTag(name="Algebra")
        db.session.add(subject_tag)
        db.session.commit()
        question = Question(
            title="What is the difference between a linear and quadratic equation?",
            difficulty=3,
            content="A linear equation has a degree of 1, while a quadratic equation has a degree of 2.",
            user=user,
            course=course,
            subject_tags=[subject_tag],
        )
        db.session.add(question)
        db.session.commit()
        assert question.uuid is not None
        assert (
            question.title
            == "What is the difference between a linear and quadratic equation?"
        )
        assert question.difficulty == 3
        assert (
            question.content
            == "A linear equation has a degree of 1, while a quadratic equation has a degree of 2."
        )
        assert question.user.username == "test_user"
        assert question.course.name == "Math 101"
        assert question.course.course_level.name == "Undergraduate"
        assert question.course.course_level.code == "UGRD"
        assert question.subject_tags[0].name == "Algebra"


def test_question_model_query(empty_app):
    with empty_app.app_context():
        user = User(
            username="test_user", email="test@example.com", password="password123"
        )
        db.session.add(user)
        course_level = CourseLevel(
            name="Undergraduate", code="UGRD", study_type="Bachelor"
        )
        db.session.add(course_level)
        course = Course(name="Math 101", code="MATH101", course_level=course_level)
        db.session.add(course)
        subject_tag = SubjectTag(name="Algebra")
        db.session.add(subject_tag)
        db.session.commit()
        question = Question(
            title="What is the difference between a linear and quadratic equation?",
            difficulty=3,
            content="A linear equation has a degree of 1, while a quadratic equation has a degree of 2.",
            user=user,
            course=course,
            subject_tags=[subject_tag],
        )
        db.session.add(question)
        db.session.commit()
        assert question.uuid is not None
        assert (
            question.title
            == "What is the difference between a linear and quadratic equation?"
        )
        assert question.difficulty == 3
        assert (
            question.content
            == "A linear equation has a degree of 1, while a quadratic equation has a degree of 2."
        )
        assert question.user.username == "test_user"
        assert question.course.name == "Math 101"
        assert question.course.course_level.name == "Undergraduate"
        assert question.course.course_level.code == "UGRD"
        assert question.subject_tags[0].name == "Algebra"

        queried_question = Question.query.filter_by(
            title="What is the difference between a linear and quadratic equation?"
        ).first()
        assert queried_question is not None
        assert queried_question.uuid == question.uuid
        assert (
            queried_question.title
            == "What is the difference between a linear and quadratic equation?"
        )
        assert queried_question.difficulty == 3
        assert (
            queried_question.content
            == "A linear equation has a degree of 1, while a quadratic equation has a degree of 2."
        )
        assert queried_question.user.username == "test_user"
        assert queried_question.course.name == "Math 101"
        assert queried_question.course.course_level.name == "Undergraduate"
        assert queried_question.course.course_level.code == "UGRD"
        assert queried_question.subject_tags[0].name == "Algebra"


def test_question_model_expose(empty_app):
    with empty_app.app_context():
        user = User(
            username="test_user", email="test@example.com", password="password123"
        )
        db.session.add(user)
        course_level = CourseLevel(
            name="Undergraduate", code="UGRD", study_type="Bachelor"
        )
        db.session.add(course_level)
        course = Course(name="Math 101", code="MATH101", course_level=course_level)
        db.session.add(course)
        subject_tag = SubjectTag(name="Algebra")
        db.session.add(subject_tag)
        db.session.commit()
        question = Question(
            title="What is the difference between a linear and quadratic equation?",
            difficulty=3,
            content="A linear equation has a degree of 1, while a quadratic equation has a degree of 2.",
            user=user,
            course=course,
            subject_tags=[subject_tag],
        )
        db.session.add(question)
        db.session.commit()
        exposed_data = question.expose()
        assert exposed_data["id"] == question.uuid
        assert (
            exposed_data["title"]
            == "What is the difference between a linear and quadratic equation?"
        )
        assert (
            exposed_data["content"]
            == "A linear equation has a degree of 1, while a quadratic equation has a degree of 2."
        )
        assert exposed_data["course"]["name"] == "Math 101"
        assert exposed_data["course"]["code"] == "MATH101"
        assert exposed_data["course"]["course_level"]["name"] == "Undergraduate"
        assert exposed_data["user"]["username"] == "test_user"
        assert exposed_data["subject_tags"][0]["name"] == "Algebra"
