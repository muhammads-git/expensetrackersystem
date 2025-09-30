from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,Email,NumberRange
from wtforms import StringField,PasswordField,EmailField,SubmitField,IntegerField,TextAreaField,DecimalField,SelectField
import datetime

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
    month = SelectField(
        "Month",
        choices=[
            ("1", "January"), ("2", "February"), ("3", "March"),
            ("4", "April"), ("5", "May"), ("6", "June"),
            ("7", "July"), ("8", "August"), ("9", "September"),
            ("10", "October"), ("11", "November"), ("12", "December")
        ],
        validators=[DataRequired()]
    )
    
    # dynamic years
    current_years = datetime.date.today().year
    # year
    years = [(str(y),str(y)) for y in range(current_years -5, current_years + 5)]

    year = SelectField('Year',choices=years, validators=[DataRequired()])
    submit = SubmitField('Generate Reports')

