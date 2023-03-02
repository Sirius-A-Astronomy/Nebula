from flask import Blueprint, jsonify

from nebula.models.subject_tag import SubjectTag
from nebula.routes.api import bp as api_bp

bp = Blueprint("subject_tag_api", __name__, url_prefix="/subject_tags")

api_bp.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def get_all_subject_tags():
    subject_tags = SubjectTag.query.all()
    return jsonify([subject_tag.expose() for subject_tag in subject_tags])
