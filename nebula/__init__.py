from flask import Flask
from config import configs
# from flask_sqlalchemy import SQLAlchemy

# db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(configs['default'])

    # db.init_app(app)

    with app.app_context():
        from app.views.main import main
        app.register_blueprint(main)

        # db.create_all()

        return app