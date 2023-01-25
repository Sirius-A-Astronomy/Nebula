import re

from passlib.hash import sha256_crypt
from sqlalchemy.ext.hybrid import hybrid_property

from nebula.models import GUID, Base, db

subscriptions = db.Table(
    "subscriptions",
    db.Column("user_uuid", GUID(), db.ForeignKey("user.uuid")),
    db.Column("subscription_uuid", GUID(), db.ForeignKey("subscription.uuid")),
    extend_existing=True,
)


class User(Base):
    """
    User model for the database.

    :param username: The username of the user. Must be unique. Case-insensitive.
    :type username: str
    :param password: The password of the user.
    :type password: str
    :param first_name: The first name of the user.
    :type first_name: str
    :param last_name: The last name of the user.
    :type last_name: str
    :param access_level: The access level of the user.
    :type access_level: int
    :param is_active: Whether the user is active or not.
    :type is_active: bool
    :param is_authenticated: Whether the user is authenticated or not.
        Is set to true when the user logs in and false when the user logs out.
    :type is_authenticated: bool
    :param is_anonymous: Whether the user is anonymous or not.
    :type is_anonymous: bool

    """

    # access_levels are defined in nebula/helpers/access_levels.py

    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    username = db.Column(db.String(128), nullable=False, unique=True)
    access_level = db.Column(db.Integer, nullable=False, default=0)
    password = db.Column(db.String(300), nullable=False)
    email = db.Column(db.String(128), nullable=True)

    is_authenticated = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    is_anonymous = db.Column(db.Boolean, default=False)

    subscriptions = db.relationship(
        "Subscription", secondary=subscriptions, backref=db.backref("users", lazy=True)
    )

    def get_id(self):
        return self.uuid

    def set_password(self, password):
        self.password = sha256_crypt.encrypt(password)
        db.session.commit()

    def check_password(self, password):
        return sha256_crypt.verify(password, self.password)

    @hybrid_property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    # email should just be: username@astro.rug.nl, no need to store it ?
    # storing email anyway in case user wants to use a different email address

    def has_access(self, required_access_level):
        """Check if the user has the required access level."""
        return self.access_level >= required_access_level

    def __repr__(self):
        return f'User("{self.username}")'

    def expose(self):
        return {
            "id": self.uuid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "access_level": self.access_level,
            "email": self.email,
            "created_at": self.created_at,
        }


def create_user(username, password, **kwargs):
    """
    Returns the created user object.

    :param username: The username of the to be created user.
    :type username: str
    :param password: The password of the to be created user.
    :type password: str
    :param kwargs: The additional arguments to pass to the user object.
    """
    hashed_password = sha256_crypt.encrypt(password)
    user = User(username=username, password=hashed_password, **kwargs)
    return user


def validate_username(username, user=None):
    """
    Validates the username to be unique.

    :param form: The form to validate.
    :type form: Form
    :param field: The field to validate.
    :type field: StringField
    """
    username = username.lower()
    if re.findall(r"\s", username):
        return False, "Please enter a username without any spaces"

    if re.search(r"[ @()+=\[\]{};\':\"\\|,.<>\/\?]", username):
        return False, "Please enter a username without any special characters"

    user_with_username = User.query.filter_by(username=username).one_or_none()
    if user_with_username is not None and user_with_username != user:
        return (
            False,
            "It looks like we already know someone with that username, do you want to try another one?",
        )

    return True, ""


def validate_email(email: str, user=None):
    """
    Validates the email to be unique. Also checks if the email is valid according to rfc2822.

    :param form: The form to validate.
    :type form: Form
    :param field: The field to validate.
    :type field: StringField
    """
    email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    if not re.match(email_regex, email):
        return (
            False,
            "We can't recognize that as an email address, please double check it",
        )

    user_with_email = User.query.filter_by(email=email).one_or_none()
    if user_with_email is not None and user_with_email != user:
        return (
            False,
            "It looks like we already know someone with that email address, do you want to try another one?",
        )

    return True, ""
