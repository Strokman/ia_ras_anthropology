from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Email, ValidationError
from anthropos import db
from anthropos.models import DatabaseUser
from anthropos.lib.validators import DataRequiredImproved

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequiredImproved(), Email(message='Введите корректный адрес электронной почты')])
    submit = SubmitField('Запросить изменение пароля')

    def validate_email(self, email):
        user = DatabaseUser.get_one_by_attr(DatabaseUser.email,
                                        email.data,
                                        db.session)
        if user is None:
            raise ValidationError("Такого пользователя не существует!")