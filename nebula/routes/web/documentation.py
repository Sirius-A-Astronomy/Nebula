from flask import Blueprint, render_template, request

from nebula.routes.web import bp as web_bp

bp = Blueprint("documentation", __name__, url_prefix="/docs")

web_bp.register_blueprint(bp)


@bp.route("/")
def documentation():
    return render_template("main/documentation.html")
