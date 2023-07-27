from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError
from anthropos import db
from anthropos.models import DatabaseUser


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Запросить изменение пароля')

    def validate_email(self, email):
        user = db.session.query(DatabaseUser).filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("Такого пользователя не существует!")