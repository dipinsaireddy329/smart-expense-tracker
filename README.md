# Smart Expense Tracker

A professional, portfolio-ready expense tracking web application built with Python Flask, MySQL, Bootstrap, JavaScript, and Chart.js. It supports secure user accounts, expense CRUD, budgets, dashboards, reports, exports, and an admin panel.

## Features

- User registration, login, logout, and password hashing
- Multiple user accounts with user-specific expense records
- Add, edit, delete, search, and filter expenses
- Categories: Food, Travel, Shopping, Education, Bills, Entertainment
- Monthly budget setup with remaining budget tracking
- Dashboard cards for total expenses, monthly expenses, budget, and balance
- Recent transactions table
- Category-wise doughnut chart and monthly bar chart using Chart.js
- Monthly and yearly reports
- CSV and PDF report export
- Admin panel for user management and platform statistics
- MySQL database with foreign keys, unique constraints, and indexes
- Responsive sidebar layout using Bootstrap and custom CSS

## Tech Stack

- Backend: Python, Flask, Flask-Login, Flask-WTF, Flask-SQLAlchemy
- Database: MySQL with PyMySQL driver
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Charts: Chart.js
- PDF Export: ReportLab

## Project Structure

```text
smart-expense-tracker/
├── app/
│   ├── routes/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── expenses.py
│   │   ├── main.py
│   │   └── reports.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   ├── templates/
│   │   ├── admin/
│   │   ├── auth/
│   │   ├── errors/
│   │   ├── expenses/
│   │   ├── reports/
│   │   ├── base.html
│   │   ├── dashboard.html
│   │   └── index.html
│   ├── __init__.py
│   ├── forms.py
│   ├── models.py
│   └── utils.py
├── database/
│   ├── schema.sql
│   └── seed_data.sql
├── config.py
├── init_db.py
├── run.py
├── requirements.txt
└── README.md
```

## Setup Instructions

1. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create your environment file:

```bash
cp .env.example .env
```

4. Update `.env` with your MySQL credentials:

```env
SECRET_KEY=replace-with-a-long-random-secret
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=smart_expense_tracker
FLASK_DEBUG=True
```

5. Create and seed the MySQL database:

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p < database/seed_data.sql
```

Alternative initializer:

```bash
python init_db.py
```

The SQL seed file adds richer sample expenses. The Python initializer creates tables, categories, and an admin account.

6. Run the application:

```bash
python run.py
```

Open `http://127.0.0.1:5000`.

## Sample Login Credentials

Admin account:

```text
Email: admin@example.com
Password: admin123
```

Student demo account:

```text
Email: student@example.com
Password: user123
```

The student account is available when you import `database/seed_data.sql`.

## Database Design

Main tables:

- `users`: Stores account details, hashed passwords, and roles
- `categories`: Stores reusable expense categories
- `expenses`: Stores user expenses with category and user foreign keys
- `budgets`: Stores one budget per user, month, and year

Important constraints:

- Unique email per user
- Unique budget per user/month/year
- Cascading delete from users to expenses and budgets
- Restricted delete for categories that are used by expenses
- Positive expense amounts

## Suggested GitHub Portfolio Improvements

- Add screenshots of the dashboard, expense list, reports, and admin panel
- Add a short demo video or GIF
- Deploy on Render/Railway with a managed MySQL database
- Add unit tests for authentication and expense CRUD
- Add pagination for large expense histories

## License

This project is open for educational and portfolio use.
