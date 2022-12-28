from passlib.hash import sha256_crypt

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

    # access_levels are defined in nebula/utilities.py

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

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, password):
        self.password = sha256_crypt.encrypt(password)
        db.session.commit()

    # email should just be: username@astro.rug.nl, no need to store it ?
    # storing email anyway in case user wants to use a different email address

    def has_access(self, required_access_level):
        """Check if the user has the required access level."""
        return self.access_level >= required_access_level

    def __repr__(self):
        return f'User("{self.username}")'


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
