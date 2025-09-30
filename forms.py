from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,Email,NumberRange
from wtforms import StringField,PasswordField,EmailField,SubmitField,IntegerField,TextAreaField,DecimalField,SelectField


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
    expense_name = StringField("Expense Name", validators=[DataRequired(), Length(min=1, max=50)], render_kw={"placeholder": "Add Expense","size":20})
    expense_amount = DecimalField("Amount", validators=[DataRequired(), NumberRange(min=1)],render_kw={"placeholder": "Add Amount","size":20})
    expense_category = StringField("Category", validators=[DataRequired()],render_kw={"placeholder": "Category","size":18})
    expense_description = TextAreaField("Description", validators=[Length(max=200)],render_kw={"placeholder": "Write Description","size":20})
    submit = SubmitField('ADD')


# Report Form
class ReportForm(FlaskForm):
    month = SelectField('Month', choices=[(1,"Jan"),(2,'Feb')])
    year = SelectField('Year', choices=[(2024,'2024'),(2025,'2025')])
    submit = SubmitField('Show Reports')

    