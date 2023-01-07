from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

import json

from nebula.models.question import Question

from nebula.routes.api import bp as api_bp

from nebula import db

from nebula.helpers.access_levels import ACCESS_LEVELS

bp = Blueprint("question_api", __name__, url_prefix="/questions")

api_bp.register_blueprint(bp)

@bp.route("/", methods=["GET"])
def get_questions():
    questions = Question.query.all()
    return jsonify(
        [
            question.expose() for question in questions
        ]
    )

@bp.route("/<uuid>", methods=["GET"])
def get_question(uuid):
    question = Question.query.filter_by(uuid=uuid).one_or_none()
    if question is None:
        return jsonify({"message": "Question not found"}), 404

    return jsonify(question.expose())

@bp.route("/", methods=["POST"])
@login_required
def create_question():
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["moderator"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401
    data = request.get_json(silent=True)

    title = data.get("title")
    if title is None:
        return jsonify({"message": "Title is required"}), 400

    body = data.get("body")
    if body is None:
        return jsonify({"message": "Body is required"}), 400

    course_id = data.get("course").get("id") if data.get("course") is not None else None
    if course_id is None:
        return jsonify({"message": "Course is required"}), 400

    from nebula.models.course import Course

    if Course.query.filter_by(uuid=course_id).one_or_none() is None:
        return jsonify({"message": "Course does not exist"}), 400

    subject_tags_req = data.get("subject_tags")
    subject_tags_json = json.load(subject_tags_req) if subject_tags_req is not None or subject_tags_json != "" else None
    if subject_tags_json is not None:
        from nebula.models.subject_tag import SubjectTag

        subject_tags = []
        for subject_tag_json in subject_tags_json:
            subject_tag = SubjectTag.query.filter_by(name=subject_tag_json.get("name").lower().strip()).one_or_none()
            if subject_tag is None:
                subject_tag = SubjectTag(name=subject_tag_json.get("name").lower().strip())
                db.session.add(subject_tag)
            subject_tags.append(subject_tag)



    question = Question(
        title=title,
        body=body,
        user_uuid=current_user.uuid,
        course_uuid=course_id,
        subject_tags=subject_tags
    )

    db.session.add(question)
    db.session.commit()

    return jsonify(question.expose()), 201

@bp.route("/<uuid>", methods=["PUT"])
@login_required
def update_question(uuid):
    question = Question.query.filter_by(uuid=uuid).one_or_none()

    if question is None:
        return jsonify({"message": "Question not found"}), 404

    if current_user.uuid != question.user_uuid and not current_user.access_level >= ACCESS_LEVELS["ByName"]["moderator"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json(silent=True)

    title = data.get("title")
    if title is not None:
        question.title = title

    body = data.get("body")
    if body is not None:
        question.body = body

    course_id = data.get("course").get("id") if data.get("course") is not None else None
    if course_id is not None:
        from nebula.models.course import Course

        if Course.query.filter_by(uuid=course_id).one_or_none() is None:
            return jsonify({"message": "Course does not exist"}), 400
        
        question.course_uuid = course_id

    subject_tags_req = data.get("subject_tags")
    subject_tags_json = json.loads(subject_tags_req) if subject_tags_req is not None else None

    if subject_tags_json is not None:
        from nebula.models.subject_tag import SubjectTag

        subject_tags = []

        for subject_tag_json in subject_tags_json:
            subject_tag = SubjectTag.query.filter_by(name=subject_tag_json.get("name").lower().strip()).one_or_none()
            if subject_tag is None:
                subject_tag = SubjectTag(name=subject_tag_json.get("name").lower().strip())
                db.session.add(subject_tag)

            subject_tags.append(subject_tag)

        question.subject_tags = subject_tags
    db.session.commit()

    question = Question.query.filter_by(uuid=uuid).one_or_none()

    return jsonify(question.expose())

@bp.route("/<uuid>", methods=["DELETE"])
@login_required
def delete_question(uuid):
    question = Question.query.filter_by(uuid=uuid).one_or_none()

    if question is None:
        return jsonify({"message": "Question not found"}), 404

    if current_user.uuid != question.user_uuid and not current_user.access_level >= ACCESS_LEVELS["ByName"]["moderator"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Question deleted successfully"}), 200