import pytest
from data import comments, course_levels, courses, questions, users
from flask_login import FlaskLoginClient, login_user
from passlib.hash import sha256_crypt

from nebula import create_app, db
from nebula.models.user import User


@pytest.fixture
def app():
    """
    Creates an app which includes a database with example data. This is
    usefull to test the front end of the website, without having to specify
    data in each test.
    """
    app = create_app(config_environment="testing")

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
    app = create_app(config_environment="testing")

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
    return empty_app.test_client()


# @pytest.fixture
# def client_as_admin(client, app):
#     """
#     Returns a client with an admin user logged in.
#     """
#     admin_user = User(
#         email="admin@admin.com",
#         first_name="Admin",
#         last_name="User",
#         access_level=4,
#         password=sha256_crypt.hash("password"),
#     )

#     with app.app_context():
#         db.session.add(admin_user)
#         db.session.commit()

#     with client as scoped_client:
#         print(scoped_client.get('/api/me').data)
#         response = scoped_client.post(
#             "/api/login",
#             json={"email":"admin@admin.com", "password":"password"},
#             follow_redirects=True,
#         )
#         print(response.data)

#         response = scoped_client.get("/api/me")
#         print(response.data)
#         yield scoped_client

#         response = scoped_client.post("/api/logout", follow_redirects=True)
#         print(response.data)


@pytest.fixture
def client_as_admin(app):
    """
    Returns a client with an admin user logged in.
    """
    admin_user = User(
        email="admin@admin.com",
        first_name="Admin",
        last_name="User",
        access_level=4,
        password=sha256_crypt.hash("password"),
        is_authenticated=True,
    )
    with app.app_context():
        db.session.add(admin_user)
        db.session.commit()

        app.test_client_class = FlaskLoginClient
        client = app.test_client(user=admin_user)

        print(client.get("/api/me").data)

    yield client


@pytest.fixture
def client_as_user(app):
    """
    Returns a client with a user logged in.
    """
    user = User(
        email="user@user.com",
        first_name="User",
        last_name="User",
        access_level=1,
        password=sha256_crypt.hash("password"),
        is_authenticated=True,
    )
    with app.app_context():
        db.session.add(user)
        db.session.commit()

        app.test_client_class = FlaskLoginClient
        client = app.test_client(user=user)
    yield client
