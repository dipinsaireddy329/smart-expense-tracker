from datetime import date

from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, EmailField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional


class RegistrationForm(FlaskForm):
    name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField("Email Address", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Create Account")


class LoginForm(FlaskForm):
    email = EmailField("Email Address", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class ExpenseForm(FlaskForm):
    title = StringField("Expense Title", validators=[DataRequired(), Length(max=140)])
    amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=0.01)], places=2)
    category_id = SelectField("Category", coerce=int, validators=[DataRequired()])
    expense_date = DateField("Date", validators=[DataRequired()], default=date.today)
    payment_method = SelectField(
        "Payment Method",
        choices=[("Cash", "Cash"), ("UPI", "UPI"), ("Card", "Card"), ("Net Banking", "Net Banking"), ("Wallet", "Wallet")],
        validators=[DataRequired()],
    )
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Save Expense")


class BudgetForm(FlaskForm):
    month = SelectField("Month", coerce=int, choices=[(i, date(2026, i, 1).strftime("%B")) for i in range(1, 13)])
    year = SelectField("Year", coerce=int, choices=[(year, str(year)) for year in range(2023, 2031)])
    amount = DecimalField("Budget Amount", validators=[DataRequired(), NumberRange(min=0)], places=2)
    submit = SubmitField("Save Budget")


class SearchForm(FlaskForm):
    query = StringField("Search", validators=[Optional(), Length(max=100)])
    category_id = SelectField("Category", coerce=int, validators=[Optional()])
    month = SelectField("Month", coerce=int, validators=[Optional()])
    year = SelectField("Year", coerce=int, validators=[Optional()])
    submit = SubmitField("Filter")
