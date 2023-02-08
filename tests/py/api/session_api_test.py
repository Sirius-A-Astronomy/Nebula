import json

from nebula.models.user import User


def test_me_as_anonymous_api(client):
    response = client.get("/api/me", content_type="application/json")

    assert response.status_code == 401


def test_me_as_admin_api(client_as_admin):
    response = client_as_admin.get("/api/me", content_type="application/json")

    assert response.status_code == 200
    assert response.json["email"] == "admin@admin.com"


def test_me_as_user_api(client_as_user):
    response = client_as_user.get("/api/me", content_type="application/json")

    assert response.status_code == 200
    assert response.json["email"] == "user@user.com"
