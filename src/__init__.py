import os
from flask import Flask
from .routes import routes
from .models import db

def create_app():
    is_serverless = os.getenv('VERCEL') or os.getenv('AWS_LAMBDA_FUNCTION_NAME')
    
    if is_serverless:
        instance_path = '/tmp'
        default_db = 'sqlite:////tmp/app.db'
    else:
        instance_path = None
        default_db = 'sqlite:///app.db'

    if instance_path:
        app = Flask(__name__, instance_path=instance_path)
    else:
        app = Flask(__name__)

    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', default_db)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'visionary_health_tracker_secret_key')

    db.init_app(app)
    app.register_blueprint(routes)

    with app.app_context():
        try:
            db.create_all()
        except Exception:
            pass

    return app