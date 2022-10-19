from flask import render_template, request, Blueprint

bp = Blueprint('documentation', __name__, url_prefix="/docs")


@bp.route('/')
def documentation():
    return render_template('main/documentation.html')
