from config import Config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    with app.app_context():
        db.init_app(app)

        if db.engine.url.drivername == "sqlite":
            migrate.init_app(app, db, render_as_batch=True, compare_type=True)
        else:
            migrate.init_app(app, db, compare_type=True)

        ma.init_app(app)
        jwt.init_app(app)
        cors.init_app(app)
        limiter.init_app(app)

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.auth import bp as auth_bp
    # Set the rate limit for all routes in the auth_bp blueprint to 1 per second
    limiter.limit("1 per second")(auth_bp)
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix='/api')

    return app
