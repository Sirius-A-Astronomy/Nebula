"""
    Creates the views for user account related pages.

    It handles:
        User login
        User registration
        User profile
        User logout
"""

from wtforms import PasswordField, StringField, SubmitField, Form, ValidationError
from wtforms.validators import DataRequired, EqualTo, Email
from flask import Blueprint, render_template, request, redirect, url_for, abort, session, jsonify
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
apibp = Blueprint("api", __name__, url_prefix="/api")


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


def validate_username(form, field):
    """
    Validates the username to be unique.

    :param form: The form to validate.
    :type form: Form
    :param field: The field to validate.
    :type field: StringField
    """
    print(field.data.lower())
    if User.query.filter_by(username=field.data.lower()).first() is not None:
        raise ValidationError(
            "It looks like we already know someone with that username, do you want to try another one?")


class RegisterForm(Form):
    """Form for registering a new user"""
    username = StringField(
        "Username",
        validators=[
            DataRequired(
                "Please enter a username, you will use this to log in"),
            validate_username])
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired(
                "Please enter your first name"
            )])
    last_name = StringField(
        "Last Name",
        validators=[
            DataRequired(
                "Please enter your last name"
            )])
    email = StringField(
        "Email",
        validators=[
            DataRequired(
                "Please enter your email address"
            ), Email(
                "We can't recognise that as an email address, please double check it"
            )
        ])

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(
                "Please enter a password."
            )])
    password_confirm = PasswordField("Confirm Password", validators=[
        DataRequired(
            "Please confirm your password"),
        EqualTo("password",
                message="Please double check that your passwords match")])
    register_submit = SubmitField("Register")


@ bp.route("/register", methods=['GET', 'POST'])
def register():
    """Creates the register page."""
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    register_form = RegisterForm(request.form)

    if request.method == 'POST' and register_form.validate():

        username = register_form.username.data.lower()
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        password = register_form.password.data

        user = create_user(username=username, first_name=first_name,
                           last_name=last_name, password=password)
        session.permanent = True
        db.session.add(user)
        user.is_authenticated = True
        db.session.commit()
        login_user(user)

        return redirect(url_for('main.index'))

        # return render_template("main/register.html", success=True, user=user)
    return render_template("main/register.html", form=register_form)


class LoginForm(Form):
    """Form for user login."""
    username = StringField("Username", validators=[DataRequired(
        "Please enter your username")])
    password = PasswordField("Password", validators=[DataRequired(
        "Please enter your password")])
    login_submit = SubmitField("Login")


@ bp.route("/login", methods=["GET", "POST"])
def login(next=None):
    """Creates the login page."""
    login_form = LoginForm(request.form)
    next = request.args.get('next')
    if request.method == "POST" and login_form.validate():
        username = login_form.username.data.lower()
        password = login_form.password.data
        valid_credentials = authenticate(username, password)

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


@ bp.route("/login-register", methods=["GET", "POST"])
def login_register(next=None, register=None):
    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)
    next = request.args.get('next')
    register = request.args.get('register')

    if request.method == "POST":

        if (login_form.login_submit.data == True):
            # Login form handling
            if login_form.validate():
                username = login_form.username.data.lower()
                password = login_form.password.data
                valid_credentials = authenticate(username, password)

                if valid_credentials:
                    session.permanent = True
                    valid_credentials.is_authenticated = login_user(
                        valid_credentials)
                    db.session.commit()
                else:
                    login_form.username.errors.append(
                        "Invalid username or password")
                    login_form.password.errors.append(
                        "Invalid username or password")
                    return render_template("main/login_register.html",
                                           login_form=login_form,
                                           register_form=register_form,
                                           next=next,
                                           register='false')
        elif register_form.validate():
            # Register form handling
            username = register_form.username.data.lower()
            first_name = register_form.first_name.data
            last_name = register_form.last_name.data
            password = register_form.password.data

            user = create_user(username=username, first_name=first_name,
                               last_name=last_name, password=password)
            session.permanent = True
            db.session.add(user)
            user.is_authenticated = True
            db.session.commit()
            login_user(user)
        else:
            return render_template("main/login_register.html",
                                   login_form=login_form,
                                   register_form=register_form,
                                   register='true')
        # redirect to next url if it is safe
        if not is_safe_url(next, request):
            return abort(400)
        return redirect(next or url_for("main.index"))
    return render_template("main/login_register.html",
                           login_form=login_form,
                           register_form=register_form,
                           next=next,
                           register=register)


@ bp.route("/logout")
def logout():
    """Logs out the current user."""
    if current_user.is_anonymous:
        return redirect(url_for("main.index"))
    user_uuid = current_user.uuid

    user = User.query.filter_by(uuid=user_uuid).first()
    logout_user()
    if user.is_authenticated:
        user.is_authenticated = False
        db.session.commit()
    return redirect(url_for("main.index"))


@ bp.route("/profile")
def profile():
    """Creates the profile page for the current user."""

    return render_template("main/profile.html")


@ apibp.route("/is_username_available", methods=["post", "GET"])
def is_username_available():
    """Returns true if the username is available."""
    if request.method == "POST":
        request_data = request.get_json()
        username = request_data["username"].lower()
        if User.query.filter_by(username=username).one_or_none() is None:
            return jsonify({"available": True})
        return jsonify({"available": False})
    return "Not a valid request"
