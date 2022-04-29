from wtforms import PasswordField, StringField, SubmitField, ValidationError, Form, SelectField
from wtforms.validators import DataRequired, EqualTo
from flask import Blueprint, render_template, request

from nebula.models import User
from nebula.account_manager import login

bp = Blueprint("login", __name__)


class LoginForm(Form):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


@bp.route("/login")
def login():

    login_form = LoginForm(request.form)
    if request.method == "POST" and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        acces_token = login(username=username, password=password)

    return render_template("login.html")
