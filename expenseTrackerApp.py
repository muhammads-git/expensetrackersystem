from flask import Flask, session, url_for, redirect, request, render_template, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
from forms import RegisterForm, LoginForm, addExpenseForm
from flask_bcrypt import Bcrypt
import time

app = Flask(__name__)

# configure the app with flask
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'muhammad'
app.config['MYSQL_PASSWORD'] = 'Shahzib123!'
app.config['MYSQL_DB'] = 'expensetracker'
app.config['SECRET_KEY'] = 'secretkeyishere'
mysql = MySQL(app)
bcrypt = Bcrypt(app)


# ---------------- REGISTER -----------------
@app.route('/')
def dashboard():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # hash the password
        hash_password = bcrypt.generate_password_hash(password).decode('utf-8')

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO user_login (username,password,email) VALUES (%s,%s,%s)',
            (username, hash_password, email),
        )
        mysql.connection.commit()
        cursor.close()
        flash('User has been successfully registered', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# ---------------- LOGIN -----------------
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_login WHERE username = %s', (username,))
        user_data = cursor.fetchone()

        if 'tries' not in session:
            session['tries'] = 0

        if user_data:
            hashed_password = user_data[3]
            if bcrypt.check_password_hash(hashed_password, password):
                session['tries'] = 0
                session['user_id'] = user_data[0]
                flash('Successfully logged in', 'success')
                return redirect(url_for('add_expense'))
            else:
                session['tries'] += 1
                if session['tries'] == 2:
                    flash('Last try', 'warning')
                if session['tries'] >= 3:
                    session['current_time'] = time.time()
                    flash('Tries limit exceeded', 'warning')
                    return redirect(url_for('site_blocked'))
                else:
                    flash('Incorrect password', 'warning')
                    return redirect(url_for('login'))

        flash('No user found', 'danger')
        return redirect(url_for('register'))

    return render_template('login.html', form=form)


@app.route('/block_user')
def site_blocked():
    time_then = session.get('current_time')
    now_time = time.time()

    wait_seconds = 90
    elapsed_time = now_time - time_then
    if elapsed_time >= wait_seconds:
        session['tries'] = 0
        session.pop('tries', None)
        return redirect(url_for('login'))
    else:
        remaining_time = int(wait_seconds - elapsed_time)
        return render_template('block_user.html', remainingTime=remaining_time)


# ---------------- EXPENSES -----------------
@app.route('/add_expenses', methods=['POST', 'GET'])
def add_expense():
    form = addExpenseForm()

    if form.validate_on_submit():
        expenseName = form.expense_name.data.capitalize()
        expenseAmount = form.expense_amount.data
        expenseCategory = form.expense_category.data.capitalize()
        expenseDescription = form.expense_description.data.capitalize()

        cursor = mysql.connection.cursor()
        cursor.execute(
            'INSERT INTO expenses (user_id,expense_name,amount,category,description) VALUES (%s,%s,%s,%s,%s)',
            (
                session['user_id'],
                expenseName,
                expenseAmount,
                expenseCategory,
                expenseDescription,
            ),
        )
        mysql.connection.commit()
        cursor.close()

        flash('Expense added successfully', 'success')
        return redirect(url_for('show_expenses'))

    return render_template('addExpenses.html', form=form)


@app.route('/show_expenses', methods=['GET'])
def show_expenses():
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT id,expense_name,amount,category,description FROM expenses WHERE user_id=%s',
        (session['user_id'],),
    )
    expense_data = cursor.fetchall()
    return render_template('show_expenses.html', expense_data=expense_data)


# ---------------- EDIT & UPDATE -----------------
@app.route('/edit_expense/<int:id>', methods=['GET'])
def edit_expense(id):
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT id,expense_name,amount,category,description FROM expenses WHERE id=%s AND user_id=%s',
        (id, session['user_id']),
    )
    expense = cursor.fetchone()
    cursor.close()

    if not expense:
        return "Expense not found or doesn't belong to the user", 404

    # Pre-fill form with current data
    form = addExpenseForm()
    form.expense_name.data = expense[1]
    form.expense_amount.data = expense[2]
    form.expense_category.data = expense[3]
    form.expense_description.data = expense[4]

    return render_template('Update_expense.html', form=form, id=id)


@app.route('/update_expenses/<int:id>', methods=['POST'])
def update_expenses(id):
    form = addExpenseForm()
    if form.validate_on_submit():
        new_expense = form.expense_name.data.capitalize()
        new_amount = form.expense_amount.data
        new_category = form.expense_category.data.capitalize()
        new_description = form.expense_description.data.capitalize()

        cursor = mysql.connection.cursor()
        cursor.execute(
            'UPDATE expenses SET expense_name=%s, amount=%s, category=%s, description=%s WHERE id=%s AND user_id=%s',
            (new_expense, new_amount, new_category, new_description, id, session['user_id']),
        )
        mysql.connection.commit()
        cursor.close()

        flash('Expense updated successfully', 'success')
        return redirect(url_for('show_expenses'))

    flash('Form validation failed. Try again!', 'danger')
    return redirect(url_for('edit_expense', id=id))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
