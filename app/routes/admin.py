from functools import wraps

from flask import Blueprint, abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import Expense, User

admin_bp = Blueprint("admin", __name__)


def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)

    return wrapped


@admin_bp.route("/")
@admin_required
def dashboard():
    total_users = User.query.count()
    total_expenses = Expense.query.count()
    total_amount = db.session.query(func.coalesce(func.sum(Expense.amount), 0)).scalar()
    top_users = (
        db.session.query(User.name, User.email, func.coalesce(func.sum(Expense.amount), 0).label("spent"))
        .outerjoin(Expense, Expense.user_id == User.id)
        .group_by(User.id, User.name, User.email)
        .order_by(func.sum(Expense.amount).desc())
        .limit(8)
        .all()
    )
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template("admin/dashboard.html", total_users=total_users, total_expenses=total_expenses, total_amount=total_amount, top_users=top_users, users=users)


@admin_bp.route("/users/<int:user_id>/toggle-admin", methods=["POST"])
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot change your own admin role.", "warning")
        return redirect(url_for("admin.dashboard"))
    user.role = "admin" if user.role == "user" else "user"
    db.session.commit()
    flash("User role updated.", "success")
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/users/<int:user_id>/delete", methods=["POST"])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You cannot delete your own account.", "warning")
        return redirect(url_for("admin.dashboard"))
    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "info")
    return redirect(url_for("admin.dashboard"))
