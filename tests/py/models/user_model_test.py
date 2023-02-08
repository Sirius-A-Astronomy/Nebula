import pytest
from passlib.hash import sha256_crypt
from sqlalchemy.exc import IntegrityError

from nebula import db
from nebula.models.user import User, validate_email


def test_create_user(empty_app):
    with empty_app.app_context():
        user = User(
            email="testuser@example.com", password=sha256_crypt.hash("testpassword")
        )
        db.session.add(user)
        db.session.commit()
        assert user.email == "testuser@example.com"
        assert user.check_password("testpassword") == True


def test_create_user_duplicate_username(empty_app):
    with empty_app.app_context():
        user = User(email="testuser@example.com", password="testpassword")
        db.session.add(user)
        db.session.commit()
        user2 = User(email="testuser@example.com", password="testpassword2")
        db.session.add(user2)
        with pytest.raises(IntegrityError):
            db.session.commit()


def test_check_password(empty_app):
    with empty_app.app_context():
        user = User(
            email="testuser@example.com", password=sha256_crypt.hash("testpassword")
        )
        db.session.add(user)
        db.session.commit()
        assert not user.check_password("wrongpassword")
        assert user.check_password("testpassword")


class TestValidateEmail:
    def test_validate_email_invalid_format(self, empty_app):
        # arrange
        email = "invalid_email"
        user = None
        with empty_app.app_context():
            # act
            result = validate_email(email, user)

        # assert
        assert result == (
            False,
            "We can't recognize that as an email address, please double check it",
        )

    def test_validate_email_already_exists(self, empty_app):
        # arrange
        email = "valid@email.com"
        user = None
        with empty_app.app_context():
            user_with_email = User(email=email, password="not important")
            db.session.add(user_with_email)
            db.session.commit()
            # act
            result = validate_email(email, user)

        # assert
        assert result == (
            False,
            "It looks like we already know someone with that email address, do you want to try another one?",
        )

    def test_validate_email_valid(self, empty_app):
        # arrange
        email = "valid@email.com"
        user = None
        with empty_app.app_context():
            # act
            result = validate_email(email, user)

        # assert
        assert result == (True, "")
