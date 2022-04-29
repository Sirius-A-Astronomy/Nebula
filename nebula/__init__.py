from flask import Flask
from config import configs
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_environment='default'):
    app = Flask(__name__)

    # Create the configuration based on the environment
    #  see config.py for specific options.
    # When you want to create an app for testing, just set the
    #  config_environment paramater to 'testing'
    app.config.from_object(configs[config_environment])

    # Initialize the database for this app (this does not create tables)
    #  this is required when multiple app 'contexts' are used
    db.init_app(app)
    jwt.init_app(app)

    # Register all the views within an app context
    with app.app_context():
        from nebula.views import main, level, course, all_courses, question, add_question, login, register
        app.register_blueprint(main.bp)
        app.register_blueprint(level.bp)
        app.register_blueprint(course.bp)
        app.register_blueprint(all_courses.bp)
        app.register_blueprint(question.bp)
        app.register_blueprint(add_question.bp)
        app.register_blueprint(login.bp)
        app.register_blueprint(register.bp)

    from nebula.context_functions import context_processor

    app.context_processor(context_processor)

    return app


# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.


# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).


# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return User.query.filter_by(uuid=identity).one_or_none()


if __name__ == "__main__":
    app = create_app()
    app.run()
