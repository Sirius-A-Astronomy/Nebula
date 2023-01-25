from data import comments, course_levels, courses, questions, users

from nebula import create_app, db
from nebula.models.comment import Comment
from nebula.models.course import Course
from nebula.models.course_level import CourseLevel
from nebula.models.question import Question
from nebula.models.user import User


def test_creation():
    """
    A Test to see if the creation of the database happens without
    exceptions and is actually empty.
    """
    app = create_app(config_environment="testing")

    with app.app_context():
        db.create_all()

        # Test that there is actually no data in the database
        assert User.query.all() == []
        assert Question.query.all() == []
        assert Comment.query.all() == []
        assert Course.query.all() == []
        assert CourseLevel.query.all() == []

        db.drop_all()  # this is important if you create the db manually


def test_data():
    """
    Tests if the data specified in data.py is all being inserted into
    the database.
    """
    app = create_app(config_environment="testing")

    with app.app_context():
        db.create_all()
        db.session.add_all(course_levels)
        db.session.add_all(courses)
        db.session.add_all(questions)
        db.session.add_all(users)
        db.session.add_all(comments)
        db.session.commit()

        assert len(CourseLevel.query.all()) == len(course_levels)
        assert len(Course.query.all()) == len(courses)
        assert len(User.query.all()) == len(users)
        assert len(Question.query.all()) == len(questions)
        assert len(Comment.query.all()) == len(comments)

        # Check if valuse are correct
        assert CourseLevel.query.filter_by(id=1).first().name == "First Year"
        assert CourseLevel.query.filter_by(id=2).first().name == "Second Year"
        assert CourseLevel.query.filter_by(id=3).first().name == "Third Year"
        assert CourseLevel.query.filter_by(id=4).first().name == "General"

        assert Course.query.filter_by(code="WILA1-06").first().name == "Linear Algebra"

        db.drop_all()
