from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from anthropos.models import DatabaseUser
from anthropos import db
from anthropos.main.forms import CleanString, OnlyCharsValidator, DataRequiredImproved


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2, max=50), DataRequired()])
    first_name = StringField(label='First Name', validators=[Length(min=2, max=50), DataRequired(), CleanString(), OnlyCharsValidator()])
    last_name = StringField(label='Last Name', validators=[Length(min=2, max=50), DataRequired(), CleanString(), OnlyCharsValidator()])
    middle_name = StringField(label='Middle Name', validators=[Length(min=0, max=50), CleanString(), OnlyCharsValidator()])
    email = StringField(label='E-Mail', validators=[Email(message='Введите корректный адрес электронной почты'), DataRequiredImproved()])
    affiliation = StringField(label='Current affiliation', validators=[Length(max=100), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Confirm password', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Create Account')

    def validate_username(self, username):
        user = db.session.query(DatabaseUser).filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('User already exists!')

    def validate_email(self, email):
        user = db.session.query(DatabaseUser).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('E-Mail already registered!')