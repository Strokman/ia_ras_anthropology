from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from anthropos.models import DatabaseUser
from anthropos import db


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[Length(min=2, max=50), DataRequired()])
    first_name = StringField(label='First Name', validators=[Length(min=2, max=50), DataRequired()])
    last_name = StringField(label='Last Name', validators=[Length(min=2, max=50), DataRequired()])
    middle_name = StringField(label='Middle Name')
    email = StringField(label='E-Mail', validators=[Email(), DataRequired()])
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