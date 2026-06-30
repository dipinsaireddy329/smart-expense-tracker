from datetime import date

from flask import Blueprint, render_template
from flask_login import current_user, login_required
from sqlalchemy import func

from app import db
from app.models import Budget, Expense
from app.utils import category_totals, current_month_window, money, monthly_series, monthly_total

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    if current_user.is_authenticated:
        return dashboard()
    return render_template("index.html")


@main_bp.route("/dashboard")
@login_required
def dashboard():
    month, year = current_month_window()
    total_expenses = money(db.session.query(func.coalesce(func.sum(Expense.amount), 0)).filter_by(user_id=current_user.id).scalar())
    monthly_expenses = monthly_total(current_user.id, month, year)
    budget = Budget.query.filter_by(user_id=current_user.id, month=month, year=year).first()
    budget_amount = money(budget.amount if budget else 0)
    remaining_budget = budget_amount - monthly_expenses
    recent_transactions = (
        Expense.query.filter_by(user_id=current_user.id).order_by(Expense.expense_date.desc(), Expense.created_at.desc()).limit(6).all()
    )
    chart_categories = category_totals(current_user.id, month, year)
    bar_series = monthly_series(current_user.id, year)

    today = date.today()
    days_in_month = today.day if (today.month == month and today.year == year) else 30
    daily_average = money(float(monthly_expenses) / days_in_month) if days_in_month > 0 else money(0)
    budget_percentage = min(int((float(monthly_expenses) / float(budget_amount) * 100)), 100) if budget_amount > 0 else 0
    top_category = chart_categories[0] if chart_categories else None

    return render_template(
        "dashboard.html",
        total_expenses=total_expenses,
        monthly_expenses=monthly_expenses,
        budget_amount=budget_amount,
        remaining_budget=remaining_budget,
        recent_transactions=recent_transactions,
        chart_categories=chart_categories,
        bar_series=bar_series,
        today=today,
        daily_average=daily_average,
        budget_percentage=budget_percentage,
        top_category=top_category,
    )
