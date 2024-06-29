from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import cloudinary

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///amco.db'
    UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
    app.config['ALLOWED_EXTENSIONS_VIDEO'] = {}
    app.config['UPLOAD_FOLDER'] = "uploads"

    # Set Cloudinary credentials
    app.config['CLOUDINARY_CLOUD_NAME'] = 'docffnxmn'
    app.config['CLOUDINARY_API_KEY'] = '286586623763179'
    app.config['CLOUDINARY_API_SECRET'] = 'BsAon9wDapIjYR0zMBQ_pWKzzAc'

    cloudinary.config(
        cloud_name=app.config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=app.config.get('CLOUDINARY_API_KEY'),
        api_secret=app.config.get('CLOUDINARY_API_SECRET')
    )

    db.init_app(app)
    migrate.init_app(app, db)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    from app.routes import register_blueprints
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app
