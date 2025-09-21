from flask_wtf import FlaskForm
from wtforms.validators import DataRequired,Length,Email
from wtforms import StringField,PasswordField,EmailField,SubmitField


class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=6,max=20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
    email = StringField('Email',validators=[DataRequired(),Email()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired(),Length(min=6,max=20)])
    password = PasswordField('Password',validators=[DataRequired(),Length(min=6,max=20)])
    submit = SubmitField('Login')
