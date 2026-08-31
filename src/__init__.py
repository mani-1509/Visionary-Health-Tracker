import os
from flask import Flask
from .routes import routes
from .models import db

def create_app():
    app = Flask(__name__)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'visionary_health_tracker_secret_key')

    db.init_app(app)
    app.register_blueprint(routes)

    return app