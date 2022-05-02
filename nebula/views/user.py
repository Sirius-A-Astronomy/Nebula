"""
    Creates the views for user account related pages.

    It handles:
        User login
        User registration
        User profile
        User logout
"""

from wtforms import PasswordField, StringField, SubmitField, Form, SelectField, ValidationError, HiddenField
from wtforms.validators import DataRequired, EqualTo
from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from flask_login import login_user, current_user, logout_user
from passlib.hash import sha256_crypt

from nebula import db, is_safe_url
from nebula.models import User

ACCESS_LEVELS = [
    (0, "Guest"),
    (1, "User"),
    (2, "Moderator"),
    (3, "Admin")
]

bp = Blueprint("user", __name__)


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


def authenticate(username, password):
    """
    Returns the user object if the credentials are valid or False otherwise.

    :param username: The username of the user.
    :type username: str
    :param password: The password of the user.
    :type password: str
    """
    user = User.query.filter_by(username=username).first()
    if user is None:
        return False
    if sha256_crypt.verify(password, user.password):
        return user
    return False


class RegisterForm(Form):
    """Form for registering a new user."""
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo("password")])
    access_level = SelectField(
        "Access Level", coerce=int, choices=ACCESS_LEVELS, validators=[DataRequired()])

    submit = SubmitField("Register")


@bp.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    register_form = RegisterForm(request.form)
    register_form.validate()
    if request.method == 'POST' and register_form.validate():
        username = register_form.username.data
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        password = register_form.password.data
        access_level = register_form.access_level.data

        user = create_user(username=username, first_name=first_name,
                           last_name=last_name, password=password, access_level=access_level)
        db.session.add(user)
        login_user(user)
        user.is_authenticated = True
        db.session.commit()

        return redirect(url_for('main.index'))

        # return render_template("main/register.html", success=True, user=user)
    return render_template("main/register.html", form=register_form)


class LoginForm(Form):
    """Form for user login."""
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@bp.route("/login", methods=["GET", "POST"])
def login(next=None):
    login_form = LoginForm(request.form)
    next = request.args.get('next')
    print(is_safe_url(next, request))
    print(f"next redirect: {next}")
    if request.method == "POST" and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        valid_credentials = authenticate(username, password)
        print(f"Valid credentials: {valid_credentials}")

        if valid_credentials:
            session.permanent = True
            valid_credentials.is_authenticated = login_user(
                valid_credentials)
            db.session.commit()
            if not is_safe_url(next, request):
                return abort(400)
            return redirect(next or url_for("main.index"))
        else:
            raise ValidationError("Invalid username or password")

    return render_template("main/login.html", form=login_form, next=next)


@bp.route("/logout")
def logout():
    if current_user.is_anonymous:
        return redirect(url_for("main.index"))
    user_uuid = current_user.uuid

    print(user_uuid)
    user = User.query.filter_by(uuid=user_uuid).first()
    logout_user()
    if user.is_authenticated:
        user.is_authenticated = False
        db.session.commit()
    return redirect(url_for("main.index"))


@bp.route("/profile")
def profile():

    return render_template("main/profile.html")
