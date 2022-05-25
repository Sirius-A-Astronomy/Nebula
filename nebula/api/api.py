import json

from flask import Flask, request, jsonify, Blueprint, url_for

from nebula.models import db, User, Question, Course
from nebula.context_functions import context_processor

pretty_date = context_processor()['pretty_date']

apibp = Blueprint('api', __name__, url_prefix='/api')


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


@ apibp.route("/get_questions", methods=["post", "GET"])
def getQuestions():
    """Returns a list of all questions"""

    questions = Question.query.all()
    questions_json = [{
        "uuid": question.uuid,
        "title": question.title,
        "content": question.content,
        "created_at": pretty_date(question.created_at),
        "url": url_for("question.question", question_uuid=question.uuid, course_code=question.course.code),
        "user": {
            "uuid": question.user.uuid,
            "username": question.user.username,
            "url": url_for("search.search", filter_by=question.user.username)
        },
        "answers_count": len(question.answers),
        "comments_count": len(question.comments),
        "course":
            {
                "uuid": question.course.uuid,
                "name": question.course.name,
                "course_code": question.course.code,
                "url":  url_for('search.search', filter_by=question.course.name)
        },
        "subject_tags": [
            {
                "name": subject_tag.name,
                "url": url_for('search.search', filter_by=subject_tag.name)

            } for subject_tag in question.subject_tags]
    } for question in questions]

    courses = Course.query.all()
    courses_json = [{
        "uuid": course.uuid,
        "name": course.name,
        "code": course.code,
        "description": course.description,
        "semester": course.semester,
        "course_level": {"code": course.course_level.code,
                         "name": course.course_level.name,
                         "study_type": course.course_level.study_type},
        "url": url_for('course.course', course_code=course.code, course_level_code=course.course_level.code),
        "questions_count": len(course.questions),
        "answers_count": sum(len(question.answers) for question in course.questions),

    } for course in courses]
    return(jsonify({"questions": questions_json, "courses": courses_json}))
