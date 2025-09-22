from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,Email
from wtforms import StringField,PasswordField,EmailField,SubmitField,IntegerField


class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=6,max=20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=6,max=20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
    submit = SubmitField('Login')


# expenses Form
class addExpenseForm(FlaskForm):
    expense_name = StringField('Add Expense', validators=[DataRequired(),Length(max=20)])
    expense_amount = IntegerField('Add Amount', validators=[DataRequired()])
    expense_category = StringField('Category',validators=[DataRequired()])
    expense_description = StringField('Description',validators=[DataRequired(),Length(max=100)])
    submit = SubmitField('ADD')

