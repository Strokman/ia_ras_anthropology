from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import Length, Email
from anthropos.models import DatabaseUser
from anthropos.lib.validators import CleanName, OnlyCharsValidator, DataRequiredImproved, CleanString


class EditProfileForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[Length(min=2, max=50), CleanString(), DataRequiredImproved()])
    first_name = StringField('Имя', validators=[Length(min=2, max=50), DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    last_name = StringField('Фамилия', validators=[Length(min=2, max=50), DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    middle_name = StringField('Отчество', validators=[Length(min=0, max=50), CleanName(), OnlyCharsValidator()])
    affiliation = StringField('Место работы', validators=[Length(min=0, max=100), CleanString(), DataRequiredImproved()])
    email = StringField(label='E-Mail', validators=[Email('Введите корректный адрес электронной почты'), DataRequiredImproved()])
    submit = SubmitField('Редактировать')

    def __init__(self, original_username, original_email, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        self.original_email = original_email

    def validate_username(self, username):
        if username.data != self.original_username:
            user = DatabaseUser.get_one_by_attr('username', self.username.data)
            if user is not None:
                raise ValidationError('Пользователь существует!')

    def validate_email(self, email):
        if email.data != self.original_email:
            user = DatabaseUser.get_one_by_attr('email', self.email.data)
            if user is not None:
                raise ValidationError('E-Mail уже зарегистрирован!')
