from flask import Flask
from flask_cors import CORS
from app.routes.admin import admin_bp

from config import Config
from app.extensions import db, jwt, migrate

from app.models import *

from app.routes.auth import auth_bp

from app.routes import (
    auth_bp,
    admin_bp,
    staff_bp,
    trekker_bp
)

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(staff_bp)
    app.register_blueprint(trekker_bp)

    return app