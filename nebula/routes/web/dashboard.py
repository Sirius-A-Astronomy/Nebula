from flask import Blueprint, render_template
from flask_login import login_required

from nebula.routes.web import bp as web_bp
from nebula.utilities import ACCESS_LEVELS

bp = Blueprint("dashboard", __name__)

web_bp.register_blueprint(bp)


@bp.route("/dashboard", defaults={"path": ""})
@bp.route("/dashboard/<path:path>")
@login_required
def index(path):
    return render_template("dashboard/index.html")