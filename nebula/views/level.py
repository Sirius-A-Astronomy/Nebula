from flask import Blueprint, render_template
bp = Blueprint('level', __name__, url_prefix='/levels')


@bp.route('/<level>')
def level(level):
    return render_template('main/level.html', level_id=level)
