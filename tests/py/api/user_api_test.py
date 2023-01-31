import json

import pytest
from flask import jsonify

from nebula import db
from nebula.models.user import User


def serializable_exposed_user(user):
    exposed_user = user.expose()
    exposed_user["id"] = str(exposed_user["id"])
    exposed_user["created_at"] = jsonify(exposed_user["created_at"]).json
    return exposed_user


def test_get_users(client_as_admin, app):
    user = User(
        username="test_admin",
        email="admin@example.com",
        first_name="Admin",
        last_name="User",
        access_level=3,
    )
    with app.app_context():
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        user_exposed = serializable_exposed_user(user)

    response = client_as_admin.get("/api/users/")

    assert response.status_code == 200
    assert user_exposed in response.json


def test_get_user_by_id(client_as_admin, app):
    user = User(
        username="test_admin",
        email="admin@admin.com",
        first_name="Admin",
        last_name="User",
        access_level=3,
    )
    with app.app_context():
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        user_exposed = serializable_exposed_user(user)

    response = client_as_admin.get(f"/api/users/{user.uuid}")
    assert response.status_code == 200
    assert response.json == user_exposed


def test_create_user(client_as_admin, app):
    response = client_as_admin.post(
        "/api/users/",
        data=json.dumps(
            {
                "username": "new_user",
                "email": "new@user.com",
                "first_name": "New",
                "last_name": "User",
                "access_level": 1,
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 201
    assert response.json["username"] == "new_user"
    assert response.json["email"] == "new@user.com"
    assert response.json["first_name"] == "New"
    assert response.json["last_name"] == "User"
    assert response.json["access_level"] == 1

    with app.app_context():
        user = User.query.filter_by(username="new_user").first()
        assert user is not None
        assert user.username == "new_user"
        assert user.email == "new@user.com"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.access_level == 1


def test_update_user(client_as_admin, app):
    user = User(
        username="test_admin",
        email="admin@admin.com",
        first_name="Admin",
        last_name="User",
        access_level=3,
    )

    with app.app_context():
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        uuid = user.uuid

    response = client_as_admin.put(
        f"/api/users/{uuid}",
        data=json.dumps(
            {
                "username": "new_user",
                "email": "new@user.com",
                "first_name": "New",
                "last_name": "User",
                "access_level": 1,
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json["username"] == "new_user"
    assert response.json["email"] == "new@user.com"
    assert response.json["first_name"] == "New"
    assert response.json["last_name"] == "User"
    assert response.json["access_level"] == 1

    with app.app_context():
        user = User.query.filter_by(username="new_user").first()
        assert user is not None
        assert user.username == "new_user"
        assert user.email == "new@user.com"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.access_level == 1


def test_delete_user(client_as_admin, app):
    user = User(
        username="test_admin",
        email="admin@admin.com",
        first_name="Admin",
        last_name="User",
        access_level=3,
    )

    with app.app_context():
        user.set_password("password")
        db.session.add(user)
        db.session.commit()

        assert User.query.filter_by(username="test_admin").first() is not None

    response = client_as_admin.delete(f"/api/users/{user.uuid}")

    assert response.status_code == 204

    with app.app_context():
        assert User.query.filter_by(username="test_admin").first() is None


def test_unauthorized_get_users(client_as_user):
    response = client_as_user.get("/api/users/")
    assert response.status_code == 401


def test_unauthorized_get_user_by_id(client_as_user, app):
    user = User(
        username="test_admin",
        email="admin@admin.com",
        first_name="Admin",
        last_name="User",
        access_level=3,
    )

    with app.app_context():
        user.set_password("password")
        db.session.add(user)
        db.session.commit()
        uuid = user.uuid

    response = client_as_user.get(f"/api/users/{uuid}")
    assert response.status_code == 401


def test_unauthorized_create_user(client_as_user):
    response = client_as_user.post(
        "/api/users/",
        data=json.dumps(
            {
                "username": "new_user",
                "email": "new@user.com",
                "first_name": "New",
                "last_name": "User",
                "access_level": 1,
                "password": "password",
                "password_confirmation": "password",
            }
        ),
        content_type="application/json",
    )

    assert response.status_code == 401
