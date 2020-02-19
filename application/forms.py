from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from application import db
from application.models import User

class RegisterForm(FlaskForm):
    email = StringField('Email: ',
        validators = [
            DataRequired(), Email()
        ]
    )
    password = PasswordField('Password: ',
        validators = [
            DataRequired()
        ]
    )
    confirm_password = PasswordField('Confirm Password: ',
        validators = [
            DataRequired(), EqualTo('password')
        ]
    )
    submit = SubmitField('OK')

    def validate_email(self, email):
        existing_users = User.query.filter_by(email=email.data).all()
        if existing_users:
            raise ValidationError('A user with that email is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email: ',
        validators = [
            DataRequired(), Email()
        ]
    )
    password = PasswordField('Password: ',
        validators = [
            DataRequired()
        ]
    )
    submit = SubmitField('OK')

    def validate_email(self, email):
        existing_users = User.query.filter_by(email=email.data).all()
        if not existing_users:
            raise ValidationError('User does not exist.')

class PostForm(FlaskForm):
    title = StringField('Title: ',
        validators = [
            DataRequired()
        ]
    )
    content = PasswordField('Content: ',
        validators = [
            DataRequired()
        ]
    )
    submit = SubmitField('OK')

