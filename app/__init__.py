from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


from config import DevelopmentConfig

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp
    from app.routes.expenses import expenses_bp
    from app.routes.main import main_bp
    from app.routes.reports import reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(expenses_bp, url_prefix="/expenses")
    app.register_blueprint(reports_bp, url_prefix="/reports")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    with app.app_context():
        try:
            db.create_all()
            from app.models import Category, User
            DEFAULT_CATEGORIES = [
                ("Food", "#ef4444", "utensils"),
                ("Travel", "#0ea5e9", "plane"),
                ("Shopping", "#a855f7", "bag-shopping"),
                ("Education", "#22c55e", "book"),
                ("Bills", "#f59e0b", "file-invoice"),
                ("Entertainment", "#14b8a6", "film"),
            ]
            for name, color, icon in DEFAULT_CATEGORIES:
                category = Category.query.filter_by(name=name).first()
                if category is None:
                    db.session.add(Category(name=name, color=color, icon=icon))
            
            admin = User.query.filter_by(email="admin@example.com").first()
            if admin is None:
                admin = User(name="Admin User", email="admin@example.com", role="admin")
                admin.set_password("admin123")
                db.session.add(admin)
            
            db.session.commit()
        except Exception as e:
            app.logger.warning(f"Database auto-initialization skipped or failed: {e}")

    return app
