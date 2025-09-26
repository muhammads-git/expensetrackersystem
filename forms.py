from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,Email,NumberRange
from wtforms import StringField,PasswordField,EmailField,SubmitField,IntegerField,TextAreaField,DecimalField


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
    expense_name = StringField("Expense Name", validators=[DataRequired(), Length(min=1, max=50)])
    expense_amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=1)])
    expense_category = StringField("Category", validators=[DataRequired()])
    expense_description = TextAreaField("Description", validators=[Length(max=200)])
    submit = SubmitField('ADD')
