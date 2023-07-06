from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Length, Email
from anthropos.models import DatabaseUser
from anthropos.lib.validators import CleanString, OnlyCharsValidator, DataRequiredImproved


class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=2, max=50), DataRequiredImproved()])
    first_name = StringField('First name', validators=[Length(min=2, max=50), DataRequiredImproved(), CleanString(), OnlyCharsValidator()])
    last_name = StringField('Last name', validators=[Length(min=2, max=50), DataRequiredImproved(), CleanString(), OnlyCharsValidator()])
    middle_name = StringField('Middle name', validators=[Length(min=0, max=50), CleanString(), OnlyCharsValidator()])
    affiliation = StringField('Current affiliation', validators=[Length(min=0, max=100)])
    email = StringField(label='E-Mail', validators=[Email('Введите корректный адрес электронной почты'), DataRequiredImproved()])
    submit = SubmitField('Submit')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = DatabaseUser.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = DatabaseUser.query.filter_by(email=self.email.data).first()
            if user is not None:
                raise ValidationError('Please use a different email.')
