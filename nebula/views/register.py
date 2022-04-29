from wtforms import PasswordField, StringField, SubmitField, ValidationError, Form, SelectField
from wtforms.validators import DataRequired, EqualTo
from flask import Blueprint, render_template, request

from nebula import db, jwt
from nebula.models import User
from nebula.account_manager import create_user, login
ACCESS_LEVELS = [
    (0, "Guest"),
    (1, "User"),
    (2, "Moderator"),
    (3, "Admin")
]


class RegisterForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])

    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField("Confirm Password", validators=[
                                     DataRequired(), EqualTo("password")])
    access_level = SelectField(
        "Access Level", coerce=int, choices=ACCESS_LEVELS, validators=[DataRequired()])

    submit = SubmitField("Register")


bp = Blueprint("register", __name__)


@bp.route("/register", methods=['GET', 'POST'])
def register():
    register_form = RegisterForm(request.form)
    print(register_form.errors)
    register_form.validate()
    print(register_form.errors)
    if request.method == 'POST' and register_form.validate():
        username = register_form.username.data
        first_name = register_form.first_name.data
        last_name = register_form.last_name.data
        password = register_form.password.data
        access_level = register_form.access_level.data

        user = create_user(username=username, first_name=first_name,
                           last_name=last_name, password=password, access_level=access_level)
        access_token = user.access_token
        db.session.add(user)
        db.session.commit()

        return access_token

        # return render_template("main/register.html", success=True, user=user)
    return render_template("main/register.html", form=register_form)
