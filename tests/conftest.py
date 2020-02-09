import pytest
from nebula import create_app
from nebula import db
from data import course_levels, courses, questions, users, comments


@pytest.fixture
def app():
    """
    Creates an app which includes a database with example data. This is
    usefull to test the front end of the website, without having to specify
    data in each test.
    """
    app = create_app(config_environment='testing')

    with app.app_context():
        db.drop_all()  # to avoid table duplication exceptions
        db.create_all()

        # add all the test data
        db.session.add_all(course_levels)
        db.session.add_all(courses)
        db.session.add_all(questions)
        db.session.add_all(users)
        db.session.add_all(comments)
        db.session.commit()

    yield app

    with app.app_context():
        db.drop_all()  # make sure to remove all information after the test


@pytest.fixture
def empty_app():
    """
    Similar to app, but does not insert any data. Usefull to test parts of the
    database in isolation.
    TODO: there is probably some refactoring oppertunity for app/empty_app, as
          they have a lot of similar/overlapping steps.
    """
    app = create_app(config_environment='testing')

    with app.app_context():
        db.drop_all()  # to avoid table duplication exceptions
        db.create_all()

    yield app

    with app.app_context():
        db.drop_all()  # make sure to remove all information after the test


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def empty_client(empty_app):
    return app.test_client()
