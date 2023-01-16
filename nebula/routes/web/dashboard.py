from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user

from nebula.routes.web import bp as web_bp
from nebula.helpers.access_levels import ACCESS_LEVELS

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard/", defaults={"path": ""})
@bp.route("/dashboard/<path:path>")
@login_required
def index(path = None):
    if not current_user.access_level >= ACCESS_LEVELS["ByName"]["moderator"]["level"]:
        flash("You do not have access to the nebula dashboard", "warning")
        return redirect('/login')

    return render_template("dashboard/index.html")
