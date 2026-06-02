from datetime import date

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import extract, or_

from app import db
from app.forms import BudgetForm, ExpenseForm, SearchForm
from app.models import Budget, Category, Expense
from app.utils import current_month_window

expenses_bp = Blueprint("expenses", __name__)


def load_category_choices(form):
    form.category_id.choices = [(category.id, category.name) for category in Category.query.order_by(Category.name).all()]


@expenses_bp.route("/")
@login_required
def list_expenses():
    form = SearchForm(request.args, meta={"csrf": False})
    categories = Category.query.order_by(Category.name).all()
    form.category_id.choices = [(0, "All Categories")] + [(category.id, category.name) for category in categories]
    form.month.choices = [(0, "All Months")] + [(i, date(2026, i, 1).strftime("%B")) for i in range(1, 13)]
    form.year.choices = [(0, "All Years")] + [(year, str(year)) for year in range(2023, 2031)]

    query = Expense.query.filter_by(user_id=current_user.id).join(Category)
    search_text = request.args.get("query", "").strip()
    category_id = request.args.get("category_id", type=int, default=0)
    month = request.args.get("month", type=int, default=0)
    year = request.args.get("year", type=int, default=0)

    if search_text:
        query = query.filter(or_(Expense.title.ilike(f"%{search_text}%"), Expense.notes.ilike(f"%{search_text}%"), Category.name.ilike(f"%{search_text}%")))
    if category_id:
        query = query.filter(Expense.category_id == category_id)
    if month:
        query = query.filter(extract("month", Expense.expense_date) == month)
    if year:
        query = query.filter(extract("year", Expense.expense_date) == year)

    expenses = query.order_by(Expense.expense_date.desc(), Expense.created_at.desc()).all()
    return render_template("expenses/list.html", expenses=expenses, form=form)


@expenses_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_expense():
    form = ExpenseForm()
    load_category_choices(form)
    if form.validate_on_submit():
        expense = Expense(
            user_id=current_user.id,
            category_id=form.category_id.data,
            title=form.title.data.strip(),
            amount=form.amount.data,
            expense_date=form.expense_date.data,
            payment_method=form.payment_method.data,
            notes=form.notes.data,
        )
        db.session.add(expense)
        db.session.commit()
        flash("Expense added successfully.", "success")
        return redirect(url_for("expenses.list_expenses"))
    return render_template("expenses/form.html", form=form, title="Add Expense")


@expenses_bp.route("/<int:expense_id>/edit", methods=["GET", "POST"])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    form = ExpenseForm(obj=expense)
    load_category_choices(form)
    if form.validate_on_submit():
        expense.title = form.title.data.strip()
        expense.amount = form.amount.data
        expense.category_id = form.category_id.data
        expense.expense_date = form.expense_date.data
        expense.payment_method = form.payment_method.data
        expense.notes = form.notes.data
        db.session.commit()
        flash("Expense updated successfully.", "success")
        return redirect(url_for("expenses.list_expenses"))
    return render_template("expenses/form.html", form=form, title="Edit Expense")


@expenses_bp.route("/<int:expense_id>/delete", methods=["POST"])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.filter_by(id=expense_id, user_id=current_user.id).first_or_404()
    db.session.delete(expense)
    db.session.commit()
    flash("Expense deleted successfully.", "info")
    return redirect(url_for("expenses.list_expenses"))


@expenses_bp.route("/budget", methods=["GET", "POST"])
@login_required
def budget():
    form = BudgetForm()
    current_month, current_year = current_month_window()
    form.month.data = form.month.data or current_month
    form.year.data = form.year.data or current_year
    if form.validate_on_submit():
        budget_record = Budget.query.filter_by(user_id=current_user.id, month=form.month.data, year=form.year.data).first()
        if budget_record is None:
            budget_record = Budget(user_id=current_user.id, month=form.month.data, year=form.year.data)
            db.session.add(budget_record)
        budget_record.amount = form.amount.data
        db.session.commit()
        flash("Monthly budget saved.", "success")
        return redirect(url_for("main.dashboard"))
    budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.year.desc(), Budget.month.desc()).all()
    return render_template("expenses/budget.html", form=form, budgets=budgets)
