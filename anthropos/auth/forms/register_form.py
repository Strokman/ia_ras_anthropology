from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from anthropos.models import DatabaseUser
from anthropos import db
from anthropos.lib import CleanName, OnlyCharsValidator, DataRequiredImproved


class RegistrationForm(FlaskForm):
    username = StringField(label='Никнейм', validators=[Length(min=2, max=50), DataRequired()])
    first_name = StringField(label='Имя', validators=[Length(min=2, max=50), DataRequired(), CleanName(), OnlyCharsValidator()])
    last_name = StringField(label='Фамилия', validators=[Length(min=2, max=50), DataRequired(), CleanName(), OnlyCharsValidator()])
    middle_name = StringField(label='Отчество', validators=[Length(min=0, max=50), CleanName(), OnlyCharsValidator()])
    email = StringField(label='E-Mail', validators=[Email(message='Введите корректный адрес электронной почты'), DataRequiredImproved()])
    affiliation = StringField(label='Место работы', validators=[Length(max=100), DataRequired()])
    password = PasswordField(label='Пароль', validators=[Length(min=8), DataRequired()])
    confirm_password = PasswordField(label='Подтверждение пароля', validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label='Создать учетную запись')

    def validate_username(self, username):
        user = db.session.query(DatabaseUser).filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Пользователь существует!')

    def validate_email(self, email):
        user = db.session.query(DatabaseUser).filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('E-Mail уже зарегистрирован!')