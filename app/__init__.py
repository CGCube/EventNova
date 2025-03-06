from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config
from .tmdb_client import TMDBClient

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize TMDB Client
    tmdb_client = TMDBClient(
        app.config['TMDB_API_KEY'],
        app.config['TMDB_READ_ACCESS_TOKEN']
    )
    app.tmdb_client = tmdb_client

    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

        from .routes import init_routes
        init_routes(app)

    return app