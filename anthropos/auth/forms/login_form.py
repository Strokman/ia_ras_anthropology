from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from anthropos.lib.validators import DataRequiredImproved
from wtforms.validators import ValidationError

from anthropos.models import DatabaseUser


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequiredImproved()])
    password = PasswordField('Пароль', validators=[DataRequiredImproved()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

    def validate_username(self, username):
        global user
        user = DatabaseUser.get_one_by_attr('username', username.data)
        if user is None:
            raise ValidationError('Неверный логин!')
        elif not user.activated:
            raise ValidationError('Email не подтвержден!')

    def validate_password(self, password):
        if user and not user.check_password(password.data):
            raise ValidationError('Неверный пароль!')