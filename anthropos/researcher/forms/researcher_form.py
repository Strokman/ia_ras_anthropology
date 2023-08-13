from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from sqlalchemy import and_

from anthropos import db
from anthropos.models import Researcher
from anthropos.lib.validators import (
    CleanName,
    OnlyCharsValidator,
    DataRequiredImproved
    )


class ResearcherForm(FlaskForm):

    last_name = StringField(label='Фамилия', validators=[DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    first_name = StringField(label='Имя', validators=[DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    middle_name = StringField(label='Отчество', validators=[CleanName(), OnlyCharsValidator()])
    affiliation = StringField(label='Место работы', validators=[DataRequiredImproved()])
    submit = SubmitField(label='Добавить исследователя')

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        researcher = db.session.query(Researcher).filter(
            and_(Researcher.first_name == self.first_name.data, Researcher.last_name == self.last_name.data)).first()
        if researcher is not None:
            self.last_name.errors.append(f'Исследователь {researcher} уже есть в базе данных!')
            return False

        return True
