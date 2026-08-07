from flask import Flask
from flask_cors import CORS

from config import Config
from app.extensions import db, jwt, migrate, cache

from app.models import *

from app.routes import (
    auth_bp,
    admin_bp,
    staff_bp,
    trekker_bp
)

from app.celery_utils import init_celery

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    cache.init_app(
        app,
        config={
            "CACHE_TYPE": "RedisCache",
            "CACHE_REDIS_HOST": "localhost",
            "CACHE_REDIS_PORT": 6379,
            "CACHE_DEFAULT_TIMEOUT": 300
        }
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(trekker_bp)

    init_celery(app)

    return app