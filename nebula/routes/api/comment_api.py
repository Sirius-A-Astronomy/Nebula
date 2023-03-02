from flask import Blueprint, jsonify, request

from nebula.models.comment import Comment
from nebula.routes.api import bp as api_bp

bp = Blueprint("comment_api", __name__, url_prefix="/comments")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_comments():
    data = request.args

    question_uuid = data.get("question")
    if question_uuid:
        comments = Comment.query.filter_by(question_uuid=question_uuid).all()
        return jsonify([comment.expose() for comment in comments])

    user_uuid = data.get("user")
    if user_uuid:
        comments = Comment.query.filter_by(user_uuid=user_uuid).all()
        return jsonify([comment.expose() for comment in comments])

    all_comments = Comment.query.all()

    return jsonify([comment.expose() for comment in all_comments])
