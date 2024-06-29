from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import cloudinary
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    # Load environment variables
    load_dotenv()

    app.secret_key = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    # Upload folder configuration
    UPLOAD_FOLDER = os.path.join(app.root_path, os.getenv('UPLOAD_FOLDER'))
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['ALLOWED_EXTENSIONS'] = set(
        os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg,gif').split(','))
    app.config['ALLOWED_EXTENSIONS_VIDEO'] = set(
        os.getenv('ALLOWED_EXTENSIONS_VIDEO', '').split(','))

    # Set Cloudinary credentials
    app.config['CLOUDINARY_CLOUD_NAME'] = os.getenv('CLOUDINARY_CLOUD_NAME')
    app.config['CLOUDINARY_API_KEY'] = os.getenv('CLOUDINARY_API_KEY')
    app.config['CLOUDINARY_API_SECRET'] = os.getenv('CLOUDINARY_API_SECRET')

    cloudinary.config(
        cloud_name=app.config.get('CLOUDINARY_CLOUD_NAME'),
        api_key=app.config.get('CLOUDINARY_API_KEY'),
        api_secret=app.config.get('CLOUDINARY_API_SECRET')
    )

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    from app.routes import register_blueprints
    register_blueprints(app)

    with app.app_context():
        db.create_all()

    return app
