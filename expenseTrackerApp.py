from flask import Flask,session,url_for,redirect,request,render_template,flash,get_flashed_messages
from flask_mysqldb import MySQL
import MySQLdb.cursors 
import os
from dotenv import load_dotenv
from forms import RegisterForm,LoginForm
from flask_bcrypt import Bcrypt
app = Flask(__name__)

# load env
load_dotenv()

# configure the app with flask
app.config['MYSQL-HOST']= os.getenv('DB-HOST')
app.config['MYSQL-USER']= os.getenv('DB-USERNAME')
app.config['MYSQL-PASSWORD']= os.getenv('DB-PASSWORD')
app.config['MYSQL-DB']= os.getenv('DB-NAME')
app.config['SECURITY-KEY']= os.getenv('SECURITY-KEY')
mysql = MySQL(app)
bcrypt = Bcrypt(app)


# dashboard
@app.route('/')
def dashboard():
    form = RegisterForm()
    return render_template('register.html',form=form)

@app.route('/register', methods=['POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data

        # hash the password before storing in db
        hash_password  = bcrypt.generate_password_hash(password).decode('utf-8')

        # db
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO user_login (username,password,email) VALUES (%s,%s,%s)',
                       (username,hash_password,email))
        
        mysql.connection.commit()
        cursor.close()
        flash(f'{username} has successfully registered','success')

        return redirect(url_for('login'))
    
    return render_template('register.html',form=form)


# login
@app.route('/login',methods=['GET,POST'])
def login():
    form = LoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.username.data

        # 1 
        # 2
        # 3


