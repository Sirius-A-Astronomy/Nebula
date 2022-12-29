from flask import Blueprint, render_template, request, redirect, url_for

from nebula.routes.web import bp as web_bp

bp = Blueprint("documentation", __name__, url_prefix="/docs", template_folder="../../../docs/.vitepress/dist", static_folder="../../../docs/.vitepress/dist/assets", static_url_path="/assets")

web_bp.register_blueprint(bp)


@bp.route("/", defaults={"_path": ""})
@bp.route("/<path:_path>")
def documentation(_path = None):
    # because of the way vitepress works, we need to redirect the root path to the index.html

    # to handle navigating to a page directly we pass the path to the index.html

    if (_path == None or _path == ""):
        return render_template("index.html")
    return redirect(url_for("web.documentation.documentation", path=_path))
