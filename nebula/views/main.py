from flask import Blueprint, render_template
bp = Blueprint('main', __name__)

_levels = [  # temp for some testing
    {
        'id': 1,
        'name': '1st Year'
    },
    {
        'id': 2,
        'name': '2nd Year'
    },
    {
        'id': 3,
        'name': '3rd Year'
    },
]


@bp.route('/')
def index():
    return render_template('main/index.html', levels=_levels)
