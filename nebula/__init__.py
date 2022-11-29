"""
    Initialises the Nebula App.

    See the config.py file for the configuration options.
    When you want to create an app for testing, just set the
    config_environment paramater to 'testing'

    Views and blueprints are registered in the app context.

    The context processor is used to make functions and variables available
    to all templates.

    The login manager is used to handle user authentication.

    The database is initialised in the app context.

    The app is returned.
"""
from urllib.parse import urlparse, urljoin
import subprocess

from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect, CSRFError

from config import configs

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_environment='default'):
    """
        Creates the app.

        :param config_environment: The environment to use for the app.
        :type config_environment: str
    """
    app = Flask(__name__)

    # Create the configuration based on the environment
    #  see config.py for specific options.
    # When you want to create an app for testing, just set the
    #  config_environment paramater to 'testing'
    app.config.from_object(configs[config_environment]())

    # set the session expiration date
    app.permanent_session_lifetime = app.config['PERMAMENT_SESSION_LIFETIME']

    # Initialize the database for this app (this does not create tables)
    #  this is required when multiple app 'contexts' are used
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register all the views within an app context
    with app.app_context():
        from nebula.views import main, level, course, all_courses, \
            question, add_question, user, search, dashboard, \
            documentation
        from nebula.api import api
        app.register_blueprint(main.bp)
        app.register_blueprint(level.bp)
        app.register_blueprint(course.bp)
        app.register_blueprint(all_courses.bp)
        app.register_blueprint(question.bp)
        app.register_blueprint(add_question.bp)
        app.register_blueprint(user.bp)
        app.register_blueprint(search.bp)
        app.register_blueprint(api.apibp)
        app.register_blueprint(dashboard.bp)
        app.register_blueprint(documentation.bp)

    from nebula.context_functions import context_processor

    app.context_processor(context_processor)

    from nebula.views.errors import pagenotfound, internalerror, badrequest
    app.register_error_handler(404, pagenotfound)
    app.register_error_handler(500, internalerror)
    app.register_error_handler(400, badrequest)
    app.register_error_handler(CSRFError, lambda e: (e.description, 400))

    # from nebula.utilities import before_request
    # app.before_request(before_request)

    login_manager.login_view = "user.login_register"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    from nebula.utilities import unauthorized_handler
    login_manager.unauthorized_handler(unauthorized_handler)

    # Compile the sass files, TODO find another way to compile sass outside of the app
    from os import environ
    if (app.env == "development" or app.env == "testing"):
        compile_sass()

    return app


@ login_manager.user_loader
def load_user(user_uuid):
    """Returns the user object to flask-login. So it can be used in templates with current_user."""
    from nebula.models import User
    print(f"Flask login got user {user_uuid}")
    return User.query.filter_by(uuid=user_uuid).one_or_none()


def is_safe_url(target, request):
    """Returns True if the target url is safe to redirect to."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
        ref_url.netloc == test_url.netloc


def compile_sass():
    """Compiles the sass files."""
    print(" * Compiling sass files...")
    try:
        subprocess.run(
            ["npx", "sass", "./nebula/static/scss/:./nebula/static/css"])
    except Exception as e:
        print(" * Error compiling sass files. Did you run 'npm install'?")
        print(e)
        return
    print(" * Sass files compiled.")


if __name__ == "__main__":
    app = create_app()
    app.run()
