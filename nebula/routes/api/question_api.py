import re

from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required

from nebula import db
from nebula.helpers.access_levels import ACCESS_LEVELS
from nebula.helpers.error_bin import ErrorBin
from nebula.models.comment import Comment
from nebula.models.question import Question
from nebula.routes.api import bp as api_bp

bp = Blueprint("question_api", __name__, url_prefix="/questions")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_questions():
    args = request.args

    course_id = args.get("course")
    if course_id:
        questions = Question.query.filter_by(course_uuid=course_id).all()
        return jsonify([question.expose() for question in questions])

    user_id = args.get("user_id")
    if user_id:
        questions = Question.query.filter_by(user_uuid=user_id).all()
        return jsonify([question.expose() for question in questions])

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

    error_bin = ErrorBin()

    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["moderator"]["level"]:
        return jsonify({"message": "Unauthorized"}), 401
    data = request.get_json(silent=True)

    title = data.get("title")
    if not title:
        error_bin.add("title", "Title is required")

    content = data.get("content")
    if not content:
        error_bin.add("content", "Content is required")

    course_id = data.get("course_id")
    if not course_id:
        error_bin.add("course_id", "Selecting a course is required")

    if course_id:
        from nebula.models.course import Course

        if Course.query.filter_by(uuid=course_id).one_or_none() is None:
            error_bin.add("course_id", "Course does not exist")

    if error_bin.has_errors():
        return (
            jsonify({"message": "Form contains errors", "errors": error_bin.get()}),
            400,
        )

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
                name=subject_tag.lower().strip()
            ).one_or_none()
            if existing_subject_tag is None:
                # create it if not
                subject_tag = SubjectTag(name=subject_tag.lower().strip())
                db.session.add(subject_tag)
            else:
                # use it if it does
                subject_tag = existing_subject_tag

            question.subject_tags.append(subject_tag)

    answers_req = data.get("answers")
    if answers_req:
        from nebula.models.answer import Answer

        for answer in answers_req:
            answer_model = Answer(
                title=answer.get("title"),
                content=answer.get("content"),
                user_uuid=current_user.uuid,
                question_uuid=question.uuid,
            )
            db.session.add(answer_model)
            question.answers.append(answer_model)

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

    course_id = data.get("course_id")
    if course_id is not None:
        from nebula.models.course import Course

        if Course.query.filter_by(uuid=course_id).one_or_none() is None:
            return jsonify({"message": "Course does not exist"}), 400

        question.course_uuid = course_id

    subject_tags_req = data.get("subject_tags")

    if subject_tags_req is not None:
        subject_tags = []
        from nebula.models.subject_tag import SubjectTag

        for subject_tag in subject_tags_req:
            # check if a subject tag with the same name exists
            existing_subject_tag = SubjectTag.query.filter_by(
                name=subject_tag.lower().strip()
            ).one_or_none()

            if existing_subject_tag is None:
                # if it doesn't create it
                existing_subject_tag = SubjectTag(name=subject_tag.lower().strip())
                db.session.add(subject_tag)

            # add it to the list of subject tags
            subject_tags.append(existing_subject_tag)

        question.subject_tags = subject_tags

    answers_req = data.get("answers")
    if answers_req:
        from nebula.models.answer import Answer

        for answer in question.answers:
            # check if the question has an answer that is not in the request
            if str(answer.uuid) not in [a.get("id") for a in answers_req]:
                # if it does delete it
                db.session.delete(answer)

        for answer in answers_req:
            # check if the answer exists

            # check if the answer id is a UUID
            if re.match(
                "^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$",
                answer.get("id"),
            ):
                # if it is check if it exists
                existing_answer = Answer.query.filter_by(
                    uuid=answer.get("id")
                ).one_or_none()
            else:
                existing_answer = None

            if existing_answer is None:
                # if it doesn't create it
                answer_model = Answer(
                    title=answer.get("title"),
                    content=answer.get("content"),
                    user_uuid=current_user.uuid,
                    question_uuid=question.uuid,
                )
                db.session.add(answer_model)
                question.answers.append(answer_model)
            else:
                # if it does update it
                existing_answer.content = answer.get("content")
                existing_answer.title = answer.get("title")

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


@bp.route("/<question_uuid>/comments", methods=["POST"])
@login_required
def create_comment(question_uuid):
    question = Question.query.filter_by(uuid=question_uuid).one_or_none()

    if question is None:
        return jsonify({"message": "Question not found"}), 404

    error_bin = ErrorBin()

    data = request.get_json(silent=True)

    content = data.get("content")
    if not content:
        error_bin.add("content", "Content is required")

    if error_bin.has_errors():
        return jsonify({"message": "Invalid request", "errors": error_bin.get()}), 400

    comment = Comment(
        content=content,
        user_uuid=current_user.uuid,
        question_uuid=question.uuid,
    )

    db.session.add(comment)
    db.session.commit()

    return jsonify(question.expose()), 201


@bp.route("/<question_uuid>/comments/<comment_uuid>", methods=["DELETE"])
@login_required
def delete_comment(question_uuid, comment_uuid):
    question = Question.query.filter_by(uuid=question_uuid).one_or_none()

    if question is None:
        return jsonify({"message": "Question not found"}), 404

    comment = Comment.query.filter_by(uuid=comment_uuid).one_or_none()

    if comment is None:
        return jsonify({"message": "Comment not found"}), 404

    if (
        current_user.uuid != comment.user_uuid
        and not current_user.access_level
        >= ACCESS_LEVELS["ByName"]["moderator"]["level"]
    ):
        return jsonify({"message": "Unauthorized"}), 401

    db.session.delete(comment)
    db.session.commit()

    return jsonify(question.expose()), 200


@bp.route("/<question_uuid>/comments/<comment_uuid>", methods=["PUT"])
@login_required
def update_comment(question_uuid, comment_uuid):
    question = Question.query.filter_by(uuid=question_uuid).one_or_none()

    if question is None:
        return jsonify({"message": "Question not found"}), 404

    comment = Comment.query.filter_by(uuid=comment_uuid).one_or_none()

    if comment is None:
        return jsonify({"message": "Comment not found"}), 404

    if (
        current_user.uuid != comment.user_uuid
        and not current_user.access_level
        >= ACCESS_LEVELS["ByName"]["moderator"]["level"]
    ):
        return jsonify({"message": "Unauthorized"}), 401

    data = request.get_json(silent=True)

    error_bin = ErrorBin()

    content = data.get("content")
    if not content:
        error_bin.add_error("content", "Content is required")

    if error_bin.has_errors():
        return jsonify({"message": "Invalid request", "errors": error_bin.get()}), 400

    comment.content = content

    db.session.commit()

    return jsonify(question.expose()), 200
