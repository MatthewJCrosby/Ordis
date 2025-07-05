import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create extensions once (shared across modules)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load database URL from .env
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL is not set!")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions with the app
    db.init_app(app)

    # Import models after db is initialized to ensure they register properly
    from . import models
    migrate.init_app(app, db)

    # Register blueprints or routes
    from .routes import bp as main_bp
    app.register_blueprint(main_bp)

    return app
