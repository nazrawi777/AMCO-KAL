# app/routes/__init__.py
from app.routes.home_routes import home_bp
from app.routes.admin_routes import admin_bp
from app.routes.product_routes import product_bp
from app.routes.vacancy_routes import vacancy_bp
from app.routes.blog_routes import blog_bp
from app.routes.action_history_routes import action_history_bp
from app.routes.team_routes import team_bp
from app.routes.upload_routes import upload_bp
from app.routes.delete_routes import delete_bp
from app.routes.user_routes import user_bp


def register_blueprints(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(vacancy_bp)
    app.register_blueprint(blog_bp)
    app.register_blueprint(action_history_bp)
    app.register_blueprint(team_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(delete_bp)
    app.register_blueprint(user_bp)
