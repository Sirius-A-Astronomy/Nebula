from flask import jsonify, request, url_for, Blueprint
from nebula.models import Course, User, Question, SubjectTag, Answer
from sqlalchemy import or_

from nebula.context_functions import pretty_date

bp = Blueprint("search_api", __name__, url_prefix="/api")


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

    print(courses)

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
            "url": url_for(
                "course.course",
                course_code=course.code,
                course_level_code=course.course_level.code,
            ),
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
        )
    ).all()

    questions_json = [
        {
            "id": question.uuid,
            "title": question.title,
            "content": question.content,
            "created_at": pretty_date(question.created_at),
            "url": url_for(
                "question.question",
                question_uuid=question.uuid,
                course_code=question.course.code,
                course_level_code=question.course.course_level.code,
            ),
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
                    "url": url_for("search.search", query=subject_tag.name),
                }
                for subject_tag in question.subject_tags
            ],
        }
        for question in questions
    ]

    return questions_json
