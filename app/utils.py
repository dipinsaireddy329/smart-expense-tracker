import csv
from calendar import month_name
from datetime import date
from decimal import Decimal
from io import BytesIO, StringIO

from flask import make_response
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from sqlalchemy import extract, func

from app import db
from app.models import Budget, Category, Expense


def money(value):
    return Decimal(value or 0).quantize(Decimal("0.01"))


def current_month_window():
    today = date.today()
    return today.month, today.year


def get_or_create_budget(user_id, month, year):
    budget = Budget.query.filter_by(user_id=user_id, month=month, year=year).first()
    if budget is None:
        budget = Budget(user_id=user_id, month=month, year=year, amount=0)
        db.session.add(budget)
        db.session.commit()
    return budget


def monthly_total(user_id, month, year):
    total = (
        db.session.query(func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == user_id)
        .filter(extract("month", Expense.expense_date) == month)
        .filter(extract("year", Expense.expense_date) == year)
        .scalar()
    )
    return money(total)


def category_totals(user_id, month=None, year=None):
    query = (
        db.session.query(Category.name, Category.color, func.coalesce(func.sum(Expense.amount), 0))
        .join(Expense, Expense.category_id == Category.id)
        .filter(Expense.user_id == user_id)
        .group_by(Category.id, Category.name, Category.color)
        .order_by(func.sum(Expense.amount).desc())
    )
    if month:
        query = query.filter(extract("month", Expense.expense_date) == month)
    if year:
        query = query.filter(extract("year", Expense.expense_date) == year)
    return [{"name": row[0], "color": row[1], "total": float(row[2])} for row in query.all()]


def monthly_series(user_id, year):
    rows = (
        db.session.query(extract("month", Expense.expense_date), func.coalesce(func.sum(Expense.amount), 0))
        .filter(Expense.user_id == user_id)
        .filter(extract("year", Expense.expense_date) == year)
        .group_by(extract("month", Expense.expense_date))
        .all()
    )
    totals = {int(month): float(total) for month, total in rows}
    return {
        "labels": [month_name[i][:3] for i in range(1, 13)],
        "values": [totals.get(i, 0) for i in range(1, 13)],
    }


def build_csv_response(expenses, filename):
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Title", "Category", "Payment Method", "Amount", "Notes"])
    for expense in expenses:
        writer.writerow([
            expense.expense_date.isoformat(),
            expense.title,
            expense.category.name,
            expense.payment_method,
            f"{expense.amount:.2f}",
            expense.notes or "",
        ])
    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "text/csv"
    return response


def build_pdf_response(expenses, title, filename):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=28, leftMargin=28, topMargin=32, bottomMargin=28)
    styles = getSampleStyleSheet()
    story = [Paragraph(title, styles["Title"]), Spacer(1, 14)]

    data = [["Date", "Title", "Category", "Method", "Amount"]]
    for expense in expenses:
        data.append([
            expense.expense_date.strftime("%d %b %Y"),
            expense.title,
            expense.category.name,
            expense.payment_method,
            f"Rs. {expense.amount:.2f}",
        ])

    table = Table(data, repeatRows=1, colWidths=[72, 180, 92, 80, 76])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
                ("ALIGN", (-1, 1), (-1, -1), "RIGHT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    story.append(table)
    doc.build(story)
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    response.headers["Content-Type"] = "application/pdf"
    return response
