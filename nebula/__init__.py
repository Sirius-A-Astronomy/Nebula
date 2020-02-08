from flask import Flask
from config import configs
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config is None:
        app.config.from_object(configs['default'])
    else:
        app.config.from_mapping(test_config)

    # db.init_app(app)

    with app.app_context():
        from nebula.views.main import main
        app.register_blueprint(main)

        # db.create_all()

        return app
