from flask import Flask
from config import configs
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    # Register all the views within an app context
    with app.app_context():
        from nebula.views import main, level
        app.register_blueprint(main.bp)
        app.register_blueprint(level.bp)

    return app
