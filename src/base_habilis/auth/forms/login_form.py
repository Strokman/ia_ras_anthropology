from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from src.base_habilis.lib.validators import DataRequiredImproved
from wtforms.validators import ValidationError

from src.repository.models import User
from src.repository import session


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequiredImproved()])
    password = PasswordField('Пароль', validators=[DataRequiredImproved()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate_username(self, username):
        global user
        user = User.get_one_by_attr('username', session, username.data)
        if user is None:
            raise ValidationError('Неверный логин!')
        elif not user.activated:
            raise ValidationError('Email не подтвержден!')

    def validate_password(self, password):
        if user and not user.check_password(password.data):
            raise ValidationError('Неверный пароль!')
