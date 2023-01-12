import json
import random

import click
from faker import Faker
from flask import Blueprint
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError

from nebula import db

fake = Faker(["en_GB", "nl_NL", "en_US"])


bp = Blueprint("cli_db", __name__, cli_group="db")


@bp.cli.command("init")
@with_appcontext
def cli_init_db():
    db.create_all()


@bp.cli.command("drop")
@with_appcontext
def cli_drop_db():
    if input("Are you sure you want to drop all database tables? (y/[n]): ") != "y":
        print("Drop cancelled")
        return
    db.drop_all()


@bp.cli.command("reset")
@with_appcontext
def cli_reset_db():
    if input("Are you sure you want to reset the database? (y/[n]): ") != "y":
        print("Reset cancelled")
        return
    db.drop_all()
    db.create_all()


@bp.cli.command("seed")
@with_appcontext
def cli_seed_db():
    from nebula.models.course import Course
    from nebula.models.course_level import CourseLevel

    json_file = open("seed_data/courses.json", "r")
    courses_json = json.load(json_file)
    json_file.close()

    for course_level in courses_json["course_levels"]:
        new_course_level = CourseLevel(
            name=course_level["name"],
            study_type=course_level["study_type"],
            code=course_level["code"],
        )

        db.session.add(new_course_level)

        for course in course_level["courses"]:
            course = Course(
                name=course["name"],
                code=course["code"],
                description=course["description"],
                course_level=new_course_level,
                semester=course["semester"],
            )

            db.session.add(course)

    try:
        db.session.commit()
    except IntegrityError as e:
        print("Error while seeding database", e)


@bp.cli.command("seed_dev")
@click.argument("target", default="all")
@with_appcontext
def cli_dev_seed_db(target):
    if target not in ["all", "users", "courses", "questions"]:
        print("Target must be one of 'all', 'users', 'courses', 'questions'")
        return

    if target == "all" or target == "users":
        seed_users()

    if target == "all" or target == "courses":
        seed_courses()

    if target == "all" or target == "questions":
        seed_questions()


def seed_users():
    from nebula.routes.web.user import create_user

    for _ in range(random.randint(5, 15)):
        user = {
            "username": fake.user_name(),
            "password": "password",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(),
            "access_level": random.randint(0, 2),
        }

        new_user = create_user(**user)

        db.session.add(new_user)

    try:
        db.session.commit()
    except IntegrityError as e:
        print("Error while seeding database", e)


def seed_courses():
    from nebula.models.course import Course
    from nebula.models.course_level import CourseLevel

    for i in range(random.randint(1, 7)):
        study_type = ["bsc", "msc"][random.randint(0, 1)]
        name = fake.job().replace("/", "||")
        course_level = {
            "name": name,
            "study_type": {"bsc": "Bachelor", "msc": "Master"}[study_type],
            "code": f"{study_type}-{name.lower().replace(' ', '-')}",
        }

        new_course_level = CourseLevel(**course_level)

        db.session.add(new_course_level)

        for i in range(random.randint(5, 15)):
            course = {
                "name": fake.job().replace("/", "||"),
                "code": fake.unique.word(),
                "description": fake.paragraph(),
                "course_level": new_course_level,
                "semester": f"{random.randint(1, 2)}{['a', 'b', ''][random.randint(0, 2)]}",
            }

            new_course = Course(**course)

            db.session.add(new_course)

    try:
        db.session.commit()
    except IntegrityError as e:
        print("Error while seeding database", e)


def seed_subject_tags():
    from nebula.models.subject_tag import SubjectTag

    for _ in range(random.randint(5, 15)):
        subject_tag = {
            "name": fake.job().replace("/", "||"),
        }

        new_subject_tag = SubjectTag(**subject_tag)

        db.session.add(new_subject_tag)

    try:
        db.session.commit()
    except IntegrityError as e:
        print("Error while seeding database", e)


def seed_questions():
    from nebula.models.answer import Answer
    from nebula.models.course import Course
    from nebula.models.question import Question
    from nebula.models.subject_tag import SubjectTag
    from nebula.models.user import User

    seed_subject_tags()

    courses = Course.query.all()
    subject_tags = SubjectTag.query.all()
    users = User.query.all()

    if len(courses) == 0 or len(users) == 0:
        raise Exception("No courses or users found")

    for _ in range(random.randint(5, 15)):
        question = {
            "title": fake.sentence() + "?",
            "content": fake.text(),
            "subject_tags": random.sample(
                subject_tags, random.randint(0, min(3, len(subject_tags)))
            ),
            "course": random.choice(courses),
            "user": random.choice(users),
        }

        new_question = Question(**question)

        # add answers

        for _ in range(random.randint(0, 3)):
            answer = {
                "title": fake.sentence(),
                "content": fake.text(),
                "sources": random.sample([fake.uri()] * 3, random.randint(0, 3)),
                "user": random.choice(users),
            }

            new_question.answers.append(Answer(**answer))

        db.session.add(new_question)

    try:
        db.session.commit()
    except IntegrityError as e:
        print("Error while seeding database", e)
