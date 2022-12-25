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
import subprocess
from urllib.parse import urljoin, urlparse

from flask import Flask, redirect, request, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFError, CSRFProtect

from config import configs

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_environment="default"):
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
    app.permanent_session_lifetime = app.config["PERMAMENT_SESSION_LIFETIME"]

    # Initialize the database for this app (this does not create tables)
    #  this is required when multiple app 'contexts' are used
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register all the views within an app context
    with app.app_context():
        from nebula.api import api, user_api, search_api
        from nebula.views import (
            add_question,
            all_courses,
            course,
            dashboard,
            documentation,
            level,
            main,
            question,
            search,
            user,
        )

        from nebula.cli import (
            user as user_cli,
            db as db_cli,
        )

        blueprints = [
            main.bp,
            level.bp,
            course.bp,
            all_courses.bp,
            question.bp,
            add_question.bp,
            user.bp,
            search.bp,
            api.bp,
            dashboard.bp,
            documentation.bp,
            user_cli.bp,
            db_cli.bp,
            user_api.bp,
            search_api.bp,
        ]

        for blueprint in blueprints:
            app.register_blueprint(blueprint)

    from nebula.context_functions import context_processor

    app.context_processor(context_processor)

    from nebula.views.errors import badrequest, internalerror, pagenotfound

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

    return app


@login_manager.user_loader
def load_user(user_uuid):
    """Returns the user object to flask-login. So it can be used in templates with current_user."""
    from nebula.models import User

    print(f"Flask login got user {user_uuid}")
    return User.query.filter_by(uuid=user_uuid).one_or_none()


def is_safe_url(target, request):
    """Returns True if the target url is safe to redirect to."""
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc


if __name__ == "__main__":
    app = create_app()
    app.run()
