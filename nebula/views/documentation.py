from flask import Blueprint, render_template, request

bp = Blueprint("documentation", __name__, url_prefix="/docs")


@bp.route("/")
def documentation():
    return render_template("main/documentation.html")
