USE smart_expense_tracker;

INSERT INTO categories (id, name, color, icon) VALUES
(1, 'Food', '#ef4444', 'utensils'),
(2, 'Travel', '#0ea5e9', 'plane'),
(3, 'Shopping', '#a855f7', 'bag-shopping'),
(4, 'Education', '#22c55e', 'book'),
(5, 'Bills', '#f59e0b', 'file-invoice'),
(6, 'Entertainment', '#14b8a6', 'film')
ON DUPLICATE KEY UPDATE color = VALUES(color), icon = VALUES(icon);

INSERT INTO users (id, name, email, password_hash, role) VALUES
(1, 'Admin User', 'admin@example.com', 'pbkdf2:sha256:1000000$admin-seed-salt$766c870d54137ef9187f503c3c5904f37fabe19b89259607b9270eb976d1f2c8', 'admin'),
(2, 'Demo Student', 'student@example.com', 'pbkdf2:sha256:1000000$user-seed-salt$26891014f529a0b53b991d123a8d75e3a131a6b189d6e1797b0f0da709587125', 'user')
ON DUPLICATE KEY UPDATE name = VALUES(name), role = VALUES(role);

INSERT INTO budgets (user_id, month, year, amount) VALUES
(1, 6, 2026, 45000.00),
(2, 6, 2026, 18000.00),
(2, 5, 2026, 16000.00)
ON DUPLICATE KEY UPDATE amount = VALUES(amount);

INSERT INTO expenses (user_id, category_id, title, amount, expense_date, payment_method, notes) VALUES
(2, 1, 'Hostel canteen lunch', 180.00, '2026-06-01', 'UPI', 'Meal with classmates'),
(2, 2, 'Metro recharge', 500.00, '2026-06-01', 'Card', 'Monthly commute'),
(2, 4, 'Data structures book', 850.00, '2026-06-02', 'UPI', 'Semester reference'),
(2, 5, 'Mobile bill', 399.00, '2026-06-03', 'Net Banking', 'Monthly plan'),
(2, 6, 'Movie ticket', 260.00, '2026-06-05', 'UPI', 'Weekend'),
(2, 3, 'Formal shirt', 1299.00, '2026-06-08', 'Card', 'Presentation day'),
(2, 1, 'Cafe snacks', 320.00, '2026-06-12', 'Cash', ''),
(2, 2, 'Bus tickets', 240.00, '2026-05-18', 'UPI', 'Home visit'),
(2, 4, 'Online course subscription', 999.00, '2026-05-22', 'Card', 'Flask project learning'),
(1, 5, 'Cloud hosting bill', 1499.00, '2026-06-04', 'Card', 'Admin sample expense');
