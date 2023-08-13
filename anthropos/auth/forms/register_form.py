from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, ValidationError
from anthropos.models import User
from anthropos.lib import CleanName, OnlyCharsValidator, DataRequiredImproved, CleanString


class RegistrationForm(FlaskForm):
    username = StringField(label='Логин', validators=[Length(min=2, max=50), CleanString(), DataRequiredImproved()])
    last_name = StringField(label='Фамилия', validators=[Length(min=2, max=50), DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    first_name = StringField(label='Имя', validators=[Length(min=2, max=50), DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    middle_name = StringField(label='Отчество', validators=[Length(min=0, max=50), CleanName(), OnlyCharsValidator()])
    email = StringField(label='E-Mail', validators=[Email(message='Введите корректный адрес электронной почты'), DataRequiredImproved()])
    affiliation = StringField(label='Место работы', validators=[Length(max=100), DataRequiredImproved()])
    password = PasswordField(label='Пароль', validators=[Length(min=8, message='Пароль должен иметь длину минимум 8 символов'), DataRequiredImproved()])
    confirm_password = PasswordField(label='Подтверждение пароля', validators=[EqualTo('password', message='Пароли не совпадают'), DataRequiredImproved()])
    submit = SubmitField(label='Создать учетную запись')

    def validate_username(self, username):
        user = User.get_one_by_attr('username', username.data)
        if user is not None:
            raise ValidationError('Пользователь существует!')

    def validate_email(self, email):
        user = User.get_one_by_attr('email', email.data)
        if user is not None:
            raise ValidationError('E-Mail уже зарегистрирован!')
        