from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, Email, EqualTo, ValidationError
from anthropos.models import DatabaseUser
from anthropos import db
from anthropos.lib import CleanName, OnlyCharsValidator, DataRequiredImproved, CleanString
from sqlalchemy import select


class RegistrationForm(FlaskForm):
    username = StringField(label='Логин', validators=[Length(min=2, max=50), CleanString(), DataRequiredImproved()])
    first_name = StringField(label='Имя', validators=[Length(min=2, max=50), DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    last_name = StringField(label='Фамилия', validators=[Length(min=2, max=50), DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    middle_name = StringField(label='Отчество', validators=[Length(min=0, max=50), CleanName(), OnlyCharsValidator()])
    email = StringField(label='E-Mail', validators=[Email(message='Введите корректный адрес электронной почты'), DataRequiredImproved()])
    affiliation = StringField(label='Место работы', validators=[Length(max=100), DataRequiredImproved()])
    password = PasswordField(label='Пароль', validators=[Length(min=8), DataRequiredImproved()])
    confirm_password = PasswordField(label='Подтверждение пароля', validators=[EqualTo('password', message='Пароли не совпадают'), DataRequiredImproved()])
    submit = SubmitField(label='Создать учетную запись')

    def validate_username(self, username):
        stmt = select(DatabaseUser).filter_by(username=username.data)
        user = db.session.scalar(stmt)
        if user is not None:
            raise ValidationError('Пользователь существует!')

    def validate_email(self, email):
        stmt = select(DatabaseUser).filter_by(email=email.data)
        user = db.session.scalar(stmt)
        if user is not None:
            raise ValidationError('E-Mail уже зарегистрирован!')