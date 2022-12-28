from flask import Blueprint, jsonify, request, url_for
from flask_login import current_user

from nebula.context_functions import pretty_date
from nebula.models import db
from nebula.models.course import Course
from nebula.models.notification import Notification
from nebula.models.question import Question
from nebula.models.subject_tag import SubjectTag
from nebula.models.user import User
from nebula.routes.api import bp


@bp.route("/is_username_available", methods=["post"])
def is_username_available():
    """Returns true if the username is available."""
    if request.method == "POST":
        request_data = request.get_json()
        username = request_data["username"].lower()
        if User.query.filter_by(username=username).one_or_none() is None:
            return jsonify({"available": True})
        return jsonify({"available": False})
    return "Not a valid request"


@bp.route("/get_questions", methods=["post", "GET"])
def getQuestions():
    """Returns a list of all questions"""

    questions = Question.query.all()
    questions_json = [
        {
            "uuid": question.uuid,
            "title": question.title,
            "content": question.content,
            "created_at": pretty_date(question.created_at),
            "url": url_for(
                "web.question.question",
                question_uuid=question.uuid,
                course_code=question.course.code,
                course_level_code=question.course.course_level.code,
            ),
            "user": {
                "uuid": question.user.uuid,
                "username": question.user.username,
                "url": url_for("web.search.search", query=question.user.username),
            },
            "answers_count": len(question.answers),
            "comments_count": len(question.comments),
            "course": {
                "uuid": question.course.uuid,
                "name": question.course.name,
                "course_code": question.course.code,
                "url": url_for(
                    "web.course.course",
                    course_code=question.course.code,
                    course_level_code=question.course.course_level.code,
                ),
            },
            "subject_tags_names": " ; ".join(
                [subject_tag.name for subject_tag in question.subject_tags]
            ),
            "subject_tags": [
                {
                    "name": subject_tag.name,
                    "url": url_for("web.search.search", query=subject_tag.name),
                }
                for subject_tag in question.subject_tags
            ],
        }
        for question in questions
    ]

    courses = Course.query.all()
    courses_json = [
        {
            "uuid": course.uuid,
            "name": course.name,
            "code": course.code,
            "description": course.description,
            "semester": course.semester,
            "course_level": {
                "code": course.course_level.code,
                "name": course.course_level.name,
                "study_type": course.course_level.study_type,
            },
            "url": url_for(
                "web.course.course",
                course_code=course.code,
                course_level_code=course.course_level.code,
            ),
            "questions_count": len(course.questions),
            "answers_count": sum(
                len(question.answers) for question in course.questions
            ),
        }
        for course in courses
    ]
    return jsonify({"questions": questions_json, "courses": courses_json})


@bp.route("/get_course_questions", methods=["post", "GET"])
def get_course_questions(course_code=None):
    """Returns a json object with all the questions from the requested course"""
    course_code = request.args.get("course_code")

    course = Course.query.filter_by(code=course_code).one_or_none()

    questions = Question.query.filter_by(course_uuid=course.uuid).all()

    questions_json = [
        {
            "uuid": question.uuid,
            "title": question.title,
            "content": question.content,
            "created_at": pretty_date(question.created_at),
            "url": url_for(
                "web.question.question",
                question_uuid=question.uuid,
                course_code=question.course.code,
                course_level_code=question.course.course_level.code,
            ),
            "user": {
                "uuid": question.user.uuid,
                "username": question.user.username,
                "url": url_for(
                    "web.course.course",
                    course_level_code=question.course.course_level.code,
                    query=question.user.username,
                    course_code=question.course.code,
                ),
            },
            "answers_count": len(question.answers),
            "comments_count": len(question.comments),
            "course": {
                "uuid": question.course.uuid,
                "name": question.course.name,
                "course_code": question.course.code,
                "url": url_for(
                    "web.course.course",
                    course_code=question.course.code,
                    course_level_code=question.course.course_level.code,
                ),
            },
            "subject_tags_names": " ; ".join(
                [subject_tag.name for subject_tag in question.subject_tags]
            ),
            "subject_tags": [
                {
                    "name": subject_tag.name,
                    "url": url_for(
                        "web.course.course",
                        course_level_code=question.course.course_level.code,
                        query=subject_tag.name,
                        course_code=question.course.code,
                    ),
                }
                for subject_tag in question.subject_tags
            ],
        }
        for question in questions
    ]

    return jsonify({"questions": questions_json})


@bp.route("/get_subject_tags", methods=["post", "GET"])
def get_subject_tags():
    """Returns a list of all subject tags"""
    subject_tags = SubjectTag.query.all()
    subject_tags_json = [
        {
            "name": subject_tag.name,
            "url": url_for("web.search.search", query=subject_tag.name),
        }
        for subject_tag in subject_tags
    ]
    return jsonify({"subject_tags": subject_tags_json})


@bp.route("mark_notification_as_read", methods=["post"])
def mark_notification_as_read():
    """Marks a notification as read"""
    request_data = request.get_json()
    notification_uuid = request_data["notification_uuid"]
    notification = Notification.query.filter_by(uuid=notification_uuid).first()
    if current_user.uuid is not notification.user.uuid:
        return jsonify(
            {"success": False, "message": "You are not the owner of this notification"}
        )
    read = request_data["read"]
    notification.is_read = read
    db.session.commit()

    return jsonify(
        {
            "success": True,
            "message": f"Notification marked as {read}",
            "read": notification.is_read,
        }
    )
