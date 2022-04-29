from flask_jwt_extended import create_access_token
from passlib.hash import sha256_crypt

from nebula import db  # , jwt
from nebula.models import User


def login(username, password):
    """Very simple check to see if the username and password are correct.
        I have no idea how naive this approach is, probably should be checked before using in production."""
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    if sha256_crypt.verify(password, user.password):
        access_level = user.access_level
        access_token = create_access_token(identity=user.uuid, additional_claims={
                                           "access_level": access_level})
        return access_token
    return False


def check_credentials(self, username, password):
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    if sha256_crypt.verify(password, user.password):
        return True


def create_user(username, password, **kwargs):
    """Returns the created user object and an access token."""
    hashed_password = sha256_crypt.encrypt(password)
    user = User(username=username, password=hashed_password, **kwargs)
    access_level = user.access_level
    access_token = create_access_token(identity=user.uuid, additional_claims={
        "access_level": access_level})
    user.access_token = access_token
    return user
