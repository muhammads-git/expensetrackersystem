from flask import Flask,session,url_for,redirect,request,render_template,flash,get_flashed_messages
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import os
from datetime import datetime
import time
from dotenv import load_dotenv
from forms import RegisterForm,LoginForm,addExpenseForm
from flask_bcrypt import Bcrypt
app = Flask(__name__)

# load env
# load_dotenv()

# configure the app with flask
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'muhammad'
app.config['MYSQL_PASSWORD'] = 'Shahzib123!'
app.config['MYSQL_DB'] = 'expensetracker'
app.config['SECRET_KEY'] = 'secretkeyishere'
mysql = MySQL(app)
bcrypt = Bcrypt(app)


# dashboard
@app.route('/')
def dashboard():
    form = RegisterForm()
    return render_template('register.html',form=form)

@app.route('/register', methods=['POST','GET'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        print(email)

        # hash the password before storing in db
        hash_password  = bcrypt.generate_password_hash(password).decode('utf-8')
        print(hash_password)

        # db
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO user_login (username,password,email) VALUES (%s,%s,%s)',(username,hash_password,email))
        mysql.connection.commit()
        cursor.close()
        flash(f'User has been successfully registered','success')
        return redirect(url_for('login'))
    
    return render_template('register.html',form=form)


# login
@app.route('/login',methods=['POST','GET'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM user_login WHERE username = %s',(username,))
        user_data = cursor.fetchone()

        if 'tries' not in session:  # create a tries variable in session if theresn't
            session['tries'] = 0  # keep it 0

        if user_data:
            hashed_password = user_data[3]
            if bcrypt.check_password_hash(hashed_password,password):
                session['tries'] = 0
                session['user_id'] = user_data[0]
                flash('Successfully login','success')
                return redirect(url_for('add_expense'))
            else:
                session['tries'] += 1
                if session['tries'] == 2:
                    flash('Last try','warning')
                if session['tries'] >= 3:
                    session['current_time']= time.time()
                    flash('Tries limit exceeded','warning')
                    return redirect(url_for('site_blocked'))
                else:
                    flash('Incorrect password','warning')
                    return redirect(url_for('login'))

        flash('No user found','danger')
        return redirect(url_for('register'))
    
    return render_template('login.html', form=form)

@app.route('/block_user')
def site_blocked():
    time_then = session.get('current_time')
    now_time = time.time()

    wait_seconds = 90
    # elapsed time 
    elapsedTime = now_time - time_then
    if elapsedTime >= 90:
        session['tries'] = 0
        session.pop('tries',None)
        return redirect(url_for('login'))
    
    else:
        remainingTime = int(elapsedTime - 90)
        return render_template('block_user.html', remainingTime=remainingTime)
    

##### expenses
@app.route('/add_expenses',methods=['POST','GET'])
def add_expense():
    form = addExpenseForm()
    
    if form.validate_on_submit():
        expenseName = form.expense_name.data.capitalize()
        expenseAmount = form.expense_amount.data
        expenseCategory = form.expense_category.data.capitalize()
        expenseDescription = form.expense_description.data.capitalize()

        # open db
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO expenses (user_id,expense_name,amount,category,description) VALUES (%s,%s,%s,%s,%s)',
                       (session['user_id'],expenseName,expenseAmount,expenseCategory,expenseDescription))
        # commit changes
        mysql.connection.commit()
        # close db
        cursor.close()

        # Flash message
        flash('Expense added successfully','success')
        return redirect(url_for('show_expenses'))
    
    return render_template('addExpenses.html',form=form)

@app.route('/show_expenses',methods=['GET'])
def show_expenses():
    # fetch data from db and return
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT id,expense_name,amount,category,description FROM expenses WHERE user_id=%s',(session['user_id'],))
    # save in variable
    expense_data = cursor.fetchall()
    return render_template('show_expenses.html', expense_data=expense_data)


app.run(debug=True,port=5000)


