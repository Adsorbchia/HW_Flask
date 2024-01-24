from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, length



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), length(min=5)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    confirm_password = PasswordField('Confirm_password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Submit')

        
