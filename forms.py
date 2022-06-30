from flask import Flask
from flask_wtf import Form, FlaskForm
from sqlalchemy import Integer, values
from wtforms import StringField, PasswordField, TextAreaField, IntegerField, SelectField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)
from models import User

# Login Form
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
