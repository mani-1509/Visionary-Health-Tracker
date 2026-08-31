import os
from flask import Flask
from src.routes import routes
from src.models import db

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'visionary_health_tracker_secret_key')

    db.init_app(app)
    app.register_blueprint(routes)
    
    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=8000, debug=True) 

