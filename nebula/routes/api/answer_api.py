from flask import Blueprint, jsonify, request

from nebula.models.answer import Answer
from nebula.routes.api import bp as api_bp

bp = Blueprint("answer_api", __name__, url_prefix="/answers")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_answers():
    data = request.args

    question_uuid = data.get("question")
    if question_uuid:
        answers = Answer.query.filter_by(question_uuid=question_uuid).all()
        return jsonify([answer.expose() for answer in answers])

    user_uuid = data.get("user")
    if user_uuid:
        answers = Answer.query.filter_by(user_uuid=user_uuid).all()
        return jsonify([answer.expose() for answer in answers])

    all_answers = Answer.query.all()

    return jsonify([answer.expose() for answer in all_answers])
