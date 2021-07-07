from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from redis import Redis
import rq
import logging
from logging.handlers import RotatingFileHandler
import os


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(
    key_func=get_remote_address, default_limits=["200 per day", "50 per hour"]
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.redis = Redis.from_url(app.config["REDIS_URL"])
    app.task_queue = rq.Queue("flask-api-queue", connection=app.redis)

    with app.app_context():
        db.init_app(app)

        # TODO: check if this is relevant for the template
        if db.engine.url.drivername == "sqlite":
            migrate.init_app(app, db, render_as_batch=True, compare_type=True)
        else:
            migrate.init_app(app, db, compare_type=True)

        ma.init_app(app)
        jwt.init_app(app)
        cors.init_app(app)
        limiter.init_app(app)

    from app.errors import bp as errors_bp
    from app.users import bp as users_bp
    from app.posts import bp as posts_bp
    from app.comments import bp as comments_bp
    from app.auth import bp as auth_bp
    from app.tasks import bp as tasks_bp

    app.register_blueprint(errors_bp)
    app.register_blueprint(users_bp, url_prefix="/api/users")
    app.register_blueprint(posts_bp, url_prefix="/api/posts")
    app.register_blueprint(comments_bp, url_prefix="/api/comments")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(tasks_bp, url_prefix="/api/tasks")

    # Set the rate limit for all routes in the auth_bp blueprint to 1 per second
    limiter.limit("60 per minute")(auth_bp)

    # Set the debuging to rotating log files and the log format and settings
    if not app.debug:
        if not os.path.exists("logs"):
            os.mkdir("logs")
        file_handler = RotatingFileHandler(
            "logs/flask_api.log", maxBytes=10240, backupCount=10
        )
        file_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
            )
        )
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Flask API startup")

    return app
