from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from .config import Config

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../templates")
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from .models.inquiry import Inquiry

    with app.app_context():
        db.create_all()

    from .routes.route import main
    app.register_blueprint(main)

    return app
