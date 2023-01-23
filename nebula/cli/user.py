import os
from getpass import getpass

import click
from flask import Blueprint

from nebula import db
from nebula.helpers.access_levels import ACCESS_LEVELS
from nebula.models.user import User, create_user

bp = Blueprint("cli_users", __name__, cli_group="user")


@bp.cli.command("create")
@click.argument("username", default="")
@click.argument("password", default="")
@click.argument("access_level", default="")
@click.argument("create_instantly", default="n")
def cli_create_user(username="", password="", access_level="", create_instantly="n"):
    user = {}
    if username == "" or not is_username_unique(username):
        while True:
            username = input("Username: ")
            if not is_username_unique(username):
                continue
            break
    if password == "":
        password = getpass("Password: ")
    if access_level == "" or not validate_access_level(access_level):
        while True:
            access_level = input("Access level: ")
            if not validate_access_level(access_level):
                continue
            access_level = get_access_level(access_level)
            break

    user["access_level"] = access_level

    if not create_instantly == "y":
        if input("Would you like to add a name? (y/[n]) ") == "y":
            user["first_name"] = input("First Name: ")
            user["last_name"] = input("Last Name: ")

        if input("Would you like to add an email? (y/[n]) ") == "y":
            user["email"] = input("Email: ")

        if input("Would you like to create this user? ([y]/n) ") == "n":
            print("User creation cancelled")
            return

    new_user = create_user(username, password, **user)
    db.session.add(new_user)
    db.session.commit()


def is_username_unique(username: str) -> bool:
    if User.query.filter_by(username=username).first() is not None:
        print(f"Username {username} already exists")
        return False
    return True


def validate_access_level(access_level: str) -> bool:
    if access_level.isdigit():
        access_level: int = int(access_level)
        if access_level in ACCESS_LEVELS["ByLevel"].keys():
            return True
    if isinstance(access_level, str):
        access_level = access_level.lower()
        if access_level in ACCESS_LEVELS["ByName"].keys():
            return True

    max_access_level = max(ACCESS_LEVELS["ByLevel"].keys())
    min_access_level = min(ACCESS_LEVELS["ByLevel"].keys())

    print(
        f"Access level must be an integer between {min_access_level} and {max_access_level} or ({', '.join(ACCESS_LEVELS['ByName'].keys())})"
    )
    return False


def get_access_level(access_level):
    if access_level.isdigit():
        access_level = int(access_level)
        return access_level

    # access_level is a string
    access_level = access_level.lower()
    return ACCESS_LEVELS["ByName"][access_level]["level"]


@bp.cli.command("edit")
@click.argument("username", default="")
def cli_edit_user(username=""):
    user = None
    if username == "":
        username = input("Enter the username of the user you'd like to edit: ")
    while True:
        user = User.query.filter_by(username=username).first()
        if user is None:
            print(f"User {username} does not exist")
            username = input("Username: ")
            continue
        break

    if input(f"Do you want to change the password for {username}? (y/[n]) ") == "y":
        user.set_password(getpass(">>> Password: "))

    if input(f"Do you want to change the access level for {username}? (y/[n]) ") == "y":
        while True:
            access_level = input(">>> Access level: ")
            if not validate_access_level(access_level):
                continue
            user.access_level = get_access_level(access_level)
            break

    if input(f"Do you want to change other details for {username}? (y/[n]) ") == "y":
        if input(">>> Would you like to change the name? (y/[n]) ") == "y":
            user.first_name = input(">>> >>> First Name: ")
            user.last_name = input(">>> >>> Last Name: ")

        if input(">>> Would you like to change the email? (y/[n]) ") == "y":
            user.email = input(">>> >>> Email: ")

    # confirm if the user wants to save the changes
    if not input(f"Do you want to save the changes for {username}? (y/[n]) ") == "y":
        print("User edit cancelled")
        return

    db.session.commit()
    print(f"User {username} edited")


@bp.cli.command("delete")
@click.argument("username")
def cli_delete_user(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        print(f"User {username} does not exist")
        return

    db.session.delete(user)
    db.session.commit()


@bp.cli.command("list")
def cli_list_users():
    users = User.query.all()
    for user in users:
        print(user)


@bp.cli.command("reset_password")
@click.argument("username", default="")
def cli_reset_password(username=""):
    user = User.query.filter_by(username=username).first()

    while True:
        if user is None:
            print(f"User {username} does not exist")
            username = input("Username: ")
            user = User.query.filter_by(username=username).first()
            continue
        break

    random_password = os.urandom(24).hex()
    user.set_password(random_password)
    print(f"New password for {username} is {random_password}")
    db.session.commit()
