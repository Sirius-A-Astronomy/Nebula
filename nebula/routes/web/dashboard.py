from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from nebula.helpers.access_levels import ACCESS_LEVELS
from nebula.routes.web import bp as web_bp

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard/", defaults={"path": ""})
@bp.route("/dashboard/<path:path>")
@login_required
def index(path=None):
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["moderator"]["level"]:
        flash("You do not have access to the nebula dashboard", "warning")
        return redirect("/login")

    return render_template("dashboard/index.html")
