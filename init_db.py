from app import create_app, db
from app.models import Category, User


DEFAULT_CATEGORIES = [
    ("Food", "#ef4444", "utensils"),
    ("Travel", "#0ea5e9", "plane"),
    ("Shopping", "#a855f7", "bag-shopping"),
    ("Education", "#22c55e", "book"),
    ("Bills", "#f59e0b", "file-invoice"),
    ("Entertainment", "#14b8a6", "film"),
]


def seed_categories():
    for name, color, icon in DEFAULT_CATEGORIES:
        category = Category.query.filter_by(name=name).first()
        if category is None:
            db.session.add(Category(name=name, color=color, icon=icon))
    db.session.commit()


def seed_admin():
    admin = User.query.filter_by(email="admin@example.com").first()
    if admin is None:
        admin = User(name="Admin User", email="admin@example.com", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()


app = create_app()

with app.app_context():
    db.create_all()
    seed_categories()
    seed_admin()
    print("Database initialized. Admin login: admin@example.com / admin123")
