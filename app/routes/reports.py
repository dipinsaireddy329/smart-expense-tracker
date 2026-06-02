from datetime import date

from flask import Blueprint, render_template, request
from flask_login import current_user, login_required
from sqlalchemy import extract

from app.models import Expense
from app.utils import build_csv_response, build_pdf_response, category_totals, monthly_series

reports_bp = Blueprint("reports", __name__)


def filtered_expenses(month=None, year=None):
    query = Expense.query.filter_by(user_id=current_user.id)
    if month:
        query = query.filter(extract("month", Expense.expense_date) == month)
    if year:
        query = query.filter(extract("year", Expense.expense_date) == year)
    return query.order_by(Expense.expense_date.desc()).all()


@reports_bp.route("/")
@login_required
def reports():
    selected_month = request.args.get("month", type=int, default=date.today().month)
    selected_year = request.args.get("year", type=int, default=date.today().year)
    expenses = filtered_expenses(selected_month, selected_year)
    categories = category_totals(current_user.id, selected_month, selected_year)
    yearly = monthly_series(current_user.id, selected_year)
    return render_template(
        "reports/index.html",
        expenses=expenses,
        categories=categories,
        yearly=yearly,
        selected_month=selected_month,
        selected_year=selected_year,
        years=range(2023, 2031),
    )


@reports_bp.route("/csv")
@login_required
def export_csv():
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    expenses = filtered_expenses(month, year)
    return build_csv_response(expenses, "expense_report.csv")


@reports_bp.route("/pdf")
@login_required
def export_pdf():
    month = request.args.get("month", type=int)
    year = request.args.get("year", type=int)
    expenses = filtered_expenses(month, year)
    return build_pdf_response(expenses, "Smart Expense Tracker Report", "expense_report.pdf")
