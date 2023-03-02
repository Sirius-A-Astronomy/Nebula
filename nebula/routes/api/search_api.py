from flask import jsonify, request, url_for
from flask_login import current_user
from sqlalchemy import or_, select
from sqlalchemy.sql.operators import ilike_op

from nebula import db
from nebula.helpers.access_levels import ACCESS_LEVELS
from nebula.helpers.global_functions import pretty_date
from nebula.models.answer import Answer
from nebula.models.course import Course
from nebula.models.question import Question
from nebula.models.subject_tag import SubjectTag
from nebula.models.user import User
from nebula.routes.api import bp


@bp.route("/search", methods=["GET"])
def search():
    """Searches for a course, course level, or user"""
    query = request.args.get("query", None)
    if query is None:
        return jsonify({"error": "query is required"}), 400

    results = {
        "courses": [],
        "users": [],
        "questions": [],
    }

    try:
        results["courses"] = search_courses(query)
        results["questions"] = search_questions(query)
        results["users"] = search_users(query)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(results), 200


def search_courses(query: str) -> list:
    """Searches for courses by name or code"""
    if not query:
        return []

    courses = Course.query.filter(
        or_(
            Course.name.ilike(f"%{query}%"),
            Course.code.ilike(f"%{query}%"),
        )
    ).all()

    course_json = [
        {
            "id": course.uuid,
            "name": course.name,
            "code": course.code,
            "description": course.description,
            "semester": course.semester,
            "course_level": {
                "code": course.course_level.code,
                "name": course.course_level.name,
                "study_type": course.course_level.study_type,
            },
            "questions_count": len(course.questions),
        }
        for course in courses
    ]

    return course_json


def search_questions(query: str) -> list:
    """Searches for questions by subject tags"""
    if not query:
        return []

    questions = Question.query.filter(
        or_(
            Question.subject_tags.any(SubjectTag.name.ilike(f"%{query}%")),
            Question.title.ilike(f"%{query}%"),
            Question.content.ilike(f"%{query}%"),
            Question.answers.any(Answer.content.ilike(f"%{query}%")),
            Question.answers.any(Answer.title.ilike(f"%{query}%")),
            Question.course.has(Course.name.ilike(f"%{query}%")),
            Question.course.has(Course.code.ilike(f"%{query}%")),
            Question.user.has(User.first_name.ilike(f"%{query}%")),
            Question.user.has(User.last_name.ilike(f"%{query}%")),
        )
    ).all()

    questions_json = [
        {
            "id": question.uuid,
            "title": question.title,
            "content": question.content,
            "created_at": pretty_date(question.created_at),
            "user": {
                "id": question.user.uuid,
                "name": f"{question.user.first_name} {question.user.last_name}",
            },
            "course": {
                "id": question.course.uuid,
                "name": question.course.name,
                "code": question.course.code,
            },
            "subject_tags": [
                {
                    "name": subject_tag.name,
                    "id": subject_tag.uuid,
                }
                for subject_tag in question.subject_tags
            ],
        }
        for question in questions
    ]

    return questions_json


def search_users(query: str) -> list:
    """Searches for users by name or email"""

    if not query:
        return []

    if (
        current_user.is_anonymous
        or not current_user.access_level
        >= ACCESS_LEVELS["ByName"]["moderator"]["level"]
    ):
        return []

    users = db.session.execute(
        db.select(User).where(
            or_(
                User.first_name.ilike(f"%{query}%"),
                User.last_name.ilike(f"%{query}%"),
                User.email.ilike(f"%{query}%"),
            )
        )
    ).scalars()

    users_json = [
        {
            "id": user.uuid,
            "name": f"{user.first_name} {user.last_name}",
            "email": user.email,
        }
        for user in users
    ]

    return users_json
