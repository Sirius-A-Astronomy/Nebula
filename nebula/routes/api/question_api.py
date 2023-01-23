import json

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from nebula import db
from nebula.helpers.access_levels import ACCESS_LEVELS
from nebula.models.question import Question
from nebula.routes.api import bp as api_bp

bp = Blueprint("question_api", __name__, url_prefix="/questions")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_questions():
    questions = Question.query.all()
    return jsonify([question.expose() for question in questions])


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

    content = data.get("content")
    if content is None:
        return jsonify({"message": "Content is required"}), 400

    course_id = data.get("course").get("id") if data.get("course") is not None else None
    if course_id is None:
        return jsonify({"message": "Course is required"}), 400

    from nebula.models.course import Course

    if Course.query.filter_by(uuid=course_id).one_or_none() is None:
        return jsonify({"message": "Course does not exist"}), 400

    question = Question(
        title=title,
        content=content,
        user_uuid=current_user.uuid,
        course_uuid=course_id,
    )

    subject_tags_req = data.get("subject_tags")
    if subject_tags_req is not None:
        from nebula.models.subject_tag import SubjectTag

        for subject_tag in subject_tags_req:
            # if it does check if the subject tag exists
            existing_subject_tag = SubjectTag.query.filter_by(
                name=subject_tag.get("name").lower().strip()
            ).one_or_none()
            if existing_subject_tag is None:
                # create it if not
                subject_tag = SubjectTag(name=subject_tag.get("name").lower().strip())
                db.session.add(subject_tag)
            else:
                # use it if it does
                subject_tag = existing_subject_tag

            question.subject_tags.append(subject_tag)

    db.session.add(question)
    db.session.commit()

    return jsonify(question.expose()), 201


@bp.route("/<uuid>", methods=["PUT"])
@login_required
def update_question(uuid):
    question = Question.query.filter_by(uuid=uuid).one_or_none()

    if question is None:
        return jsonify({"message": "Question not found"}), 404

    if (
        current_user.uuid != question.user_uuid
        and not current_user.access_level
        >= ACCESS_LEVELS["ByName"]["moderator"]["level"]
    ):
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json(silent=True)

    title = data.get("title")
    if title is not None:
        question.title = title

    content = data.get("content")
    if content is not None:
        question.content = content

    course_id = data.get("course").get("id") if data.get("course") is not None else None
    if course_id is not None:
        from nebula.models.course import Course

        if Course.query.filter_by(uuid=course_id).one_or_none() is None:
            return jsonify({"message": "Course does not exist"}), 400

        question.course_uuid = course_id

    subject_tags_req = data.get("subject_tags")

    if subject_tags_req is not None:
        from nebula.models.subject_tag import SubjectTag

        for subject_tag in subject_tags_req:
            # check if the question doesn't have a subject tag with the same name
            if (
                db.session.execute(
                    db.select(Question)
                    .where(Question.uuid == question.uuid)
                    .where(
                        Question.subject_tags.any(
                            SubjectTag.name == subject_tag.get("name").lower().strip()
                        )
                    )
                ).scalar()
                is None
            ):
                # if it does check if the subject tag exists
                existing_subject_tag = SubjectTag.query.filter_by(
                    name=subject_tag.get("name").lower().strip()
                ).one_or_none()
                if existing_subject_tag is None:
                    # create it if not
                    subject_tag = SubjectTag(
                        name=subject_tag.get("name").lower().strip()
                    )
                    db.session.add(subject_tag)
                else:
                    # use it if it does
                    subject_tag = existing_subject_tag

                question.subject_tags.append(subject_tag)

        for subject_tag in question.subject_tags:
            # check if the question has a subject tag that is not in the request
            if (
                db.session.execute(
                    db.select(SubjectTag).where(
                        SubjectTag.name.in_(
                            [
                                subject_tag.get("name").lower().strip()
                                for subject_tag in subject_tags_req
                            ]
                        )
                    )
                ).scalar()
                is None
            ):
                # if it does remove it
                question.subject_tags.remove(subject_tag)

    db.session.commit()

    question = Question.query.filter_by(uuid=uuid).one_or_none()

    return jsonify(question.expose())


@bp.route("/<uuid>", methods=["DELETE"])
@login_required
def delete_question(uuid):
    question = Question.query.filter_by(uuid=uuid).one_or_none()

    if question is None:
        return jsonify({"message": "Question not found"}), 404

    if (
        current_user.uuid != question.user_uuid
        and not current_user.access_level
        >= ACCESS_LEVELS["ByName"]["moderator"]["level"]
    ):
        return jsonify({"message": "Unauthorized"}), 401

    db.session.delete(question)
    db.session.commit()

    return jsonify({"message": "Question deleted successfully"}), 200
