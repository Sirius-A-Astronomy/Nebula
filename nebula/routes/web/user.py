"""
    Creates the views for user account related pages.

    It handles:
        User login
        User registration
        User profile
        User logout
"""

import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from passlib.hash import sha256_crypt
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length

from nebula import db, is_safe_url
from nebula.helpers.access_levels import ACCESS_LEVELS
from nebula.models.user import User, create_user
from nebula.routes.web import bp as web_bp

bp = Blueprint("user", __name__)


def authenticate(username, password):
    """
    Returns the user object if the credentials are valid.
    Returns False in all other cases.

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
    username = field.data.lower()
    if re.findall(r"\s", username):
        raise ValidationError("Please enter a username without any spaces")

    if re.match(r"[ @()+=\[\]{};\':\"\\|,.<>\/\?]", username):
        raise ValidationError("Please enter a username without any special characters")

    if User.query.filter_by(username=field.data.lower()).first() is not None:
        raise ValidationError(
            "It looks like we already know someone with that username, do you want to try another one?"
        )


def validate_email(form, field):
    """
    Validates the email to be unique. Also checks if the email is valid according to rfc2822.

    :param form: The form to validate.
    :type form: Form
    :param field: The field to validate.
    :type field: StringField
    """
    email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
    if not re.match(email_regex, field.data):
        raise ValidationError(
            "We can't recognize that as an email address, please double check it"
        )


class RegisterForm(FlaskForm):
    """Form for registering a new user"""

    username = StringField(
        "Username",
        validators=[
            DataRequired("Please enter a username, you will use this to log in"),
            Length(
                min=3,
                max=30,
                message="Please enter a username with at least 3 and at most 30 characters",
            ),
            validate_username,
        ],
    )
    first_name = StringField(
        "First Name",
        validators=[
            DataRequired("Please enter your first name"),
        ],
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired("Please enter your last name")]
    )
    email = StringField(
        "Email",
        validators=[DataRequired("Please enter your email address"), validate_email],
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired("Please enter a password."),
            Length(
                min=12,
                max=-1,
                message="Please enter a password with at least 12 characters",
            ),
        ],
    )
    password_confirm = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired("Please confirm your password"),
            EqualTo(
                "password", message="Please double check that your passwords match"
            ),
        ],
    )
    register_submit = SubmitField("Register")


class LoginForm(FlaskForm):
    """Form for user login."""

    username = StringField(
        "Username", validators=[DataRequired("Please enter your username")]
    )
    password = PasswordField(
        "Password", validators=[DataRequired("Please enter your password")]
    )
    login_submit = SubmitField("Login")


@bp.route("/register", methods=["GET", "POST"])
@bp.route("/login", methods=["GET", "POST"])
def login_register(next=None, register=None):
    next = request.args.get("next")
    if not current_user.is_anonymous:
        flash("You're already logged in.", "info")
        # redirect to next url if it is safe
        if not is_safe_url(next, request):
            flash(
                "Tried to redirect to an unsafe url, redirecting to homepage", "warning"
            )
            return redirect(url_for("web.main.index"))
        return redirect(next or url_for("web.main.index"))

    login_form = LoginForm(request.form)
    register_form = RegisterForm(request.form)
    register = request.args.get("register")
    if request.path == "/register":
        register = True

    if request.method != "POST":
        return render_template(
            "main/login_register.html",
            login_form=login_form,
            register_form=register_form,
            next=next,
            register=register,
        )

    # POST

    # Login Post
    if login_form.login_submit.data == True:
        # Login form handling
        if not login_form.validate():
            return render_template(
                "main/login_register.html",
                login_form=login_form,
                register_form=register_form,
                next=next,
                register=register,
            )

        username = login_form.username.data.lower()
        password = login_form.password.data

        valid_credentials = authenticate(username, password)
        # Returns a user object if the username and password are valid

        if not valid_credentials:
            login_form.username.errors.append("Invalid username or password")
            login_form.password.errors.append("Invalid username or password")

            # Show the login form with errors
            return render_template(
                "main/login_register.html",
                login_form=login_form,
                register_form=register_form,
                next=next,
                register="false",
            )
        # Log the user in
        session.permanent = True
        valid_credentials.is_authenticated = login_user(valid_credentials)
        db.session.commit()

    # Register Post
    elif register_form.register_submit.data == True:

        if not register_form.validate():
            return render_template(
                "main/login_register.html",
                login_form=login_form,
                register_form=register_form,
                next=next,
                register="true",
            )

        # Register form handling
        username = register_form.username.data.lower()
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        password = register_form.password.data
        email = register_form.email.data

        user = create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            email=email,
        )
        session.permanent = True
        db.session.add(user)
        user.is_authenticated = True
        db.session.commit()
        login_user(user)
    else:
        return render_template(
            "main/login_register.html",
            login_form=login_form,
            register_form=register_form,
            register=register,
        )
    # redirect to next url if it is safe
    if not is_safe_url(next, request):
        flash("Tried to redirect to an unsafe url, redirecting to homepage", "warning")
        return redirect(url_for("web.main.index"))
    return redirect(next or url_for("web.main.index"))


@bp.route("/logout", methods=["POST"])
def logout():
    """Logs out the current user."""
    if current_user.is_anonymous:
        return redirect(url_for("web.main.index"))
    user_uuid = current_user.uuid

    user = User.query.filter_by(uuid=user_uuid).first()
    logout_user()
    if user.is_authenticated:
        user.is_authenticated = False
        db.session.commit()
    return redirect(url_for("web.main.index"))


class EditProfileForm(FlaskForm):
    """Form for editing a user's profile."""

    first_name = StringField(
        "First Name", validators=[DataRequired("Please enter your first name")]
    )
    last_name = StringField(
        "Last Name", validators=[DataRequired("Please enter your last name")]
    )
    email = StringField(
        "Email",
        validators=[DataRequired("Please enter your email address"), validate_email],
    )
    edit_submit = SubmitField("Submit changes")


class ChangePasswordForm(FlaskForm):
    """Form for changing a user's password."""

    current_password = PasswordField(
        "Current Password",
        validators=[DataRequired("Please enter your current password")],
    )
    new_password = PasswordField(
        "New Password",
        validators=[
            DataRequired("Please enter a new password"),
            EqualTo(
                "new_password_confirm",
                message="Please double check that your passwords match",
            ),
        ],
    )
    new_password_confirm = PasswordField(
        "Confirm New Password",
        validators=[DataRequired("Please confirm your new password")],
    )
    change_password_submit = SubmitField("Change Password")


class ChangeUsernameForm(FlaskForm):
    """Form for changing a user's username."""

    new_username = StringField(
        "New Username",
        validators=[DataRequired("Please enter a new username"), validate_username],
    )
    password = PasswordField(
        "Password", validators=[DataRequired("Please enter your password")]
    )
    change_username_submit = SubmitField("Change Username")


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """Creates the profile page for the current user."""
    change_password_form = ChangePasswordForm(request.form)
    change_username_form = ChangeUsernameForm(request.form)
    edit_profile_form = EditProfileForm(request.form)

    if request.method == "POST":
        if change_password_form.change_password_submit.data == True:
            if not change_password_form.validate():
                return render_template(
                    "main/profile.html",
                    change_password_form=change_password_form,
                    change_username_form=change_username_form,
                    edit_profile_form=edit_profile_form,
                    access_levels=ACCESS_LEVELS,
                )

            current_password = change_password_form.current_password.data

            authenticated_user = authenticate(current_user.username, current_password)
            if not authenticated_user:
                change_password_form.current_password.errors.append(
                    "That doesn't seem to be your current password"
                )
                return render_template(
                    "main/profile.html",
                    change_password_form=change_password_form,
                    change_username_form=change_username_form,
                    edit_profile_form=edit_profile_form,
                    access_levels=ACCESS_LEVELS,
                )

            new_password = change_password_form.new_password.data
            new_password_hashed = sha256_crypt.encrypt(new_password)
            authenticated_user.password = new_password_hashed
            db.session.commit()
            flash("Password changed successfully!", "success")
            return redirect(url_for("web.user.profile"))

    return render_template(
        "main/profile.html",
        change_password_form=change_password_form,
        change_username_form=change_username_form,
        edit_profile_form=edit_profile_form,
        access_levels=ACCESS_LEVELS,
    )
