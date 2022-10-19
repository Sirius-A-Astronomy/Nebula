from flask import render_template


def pagenotfound(error):
    return render_template('errors/404.html'), 404


def internalerror(error):
    return render_template('errors/500.html'), 500


def badrequest(error):
    return render_template('errors/400.html'), 400
