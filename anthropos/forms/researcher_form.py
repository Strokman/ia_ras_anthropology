from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length
from anthropos.models import Researcher
from anthropos import db
from sqlalchemy import and_
from .validators import CleanString


class ResearcherForm(FlaskForm):

    first_name = StringField(label='First Name', validators=[Length(min=2, max=50), DataRequired(), CleanString()])
    middle_name = StringField(label='Middle Name', validators=[Length(min=2, max=50), CleanString()])
    last_name = StringField(label='Last Name', validators=[Length(min=2, max=50), DataRequired(), CleanString()])
    submit = SubmitField(label='Добавить исследователя')

    def validate(self, extra_validators=None):
        rv = FlaskForm.validate(self)
        if not rv:
            return False

        researcher = db.session.query(Researcher).filter(
            and_(Researcher.first_name == self.first_name.data, Researcher.last_name == self.last_name.data)).first()
        if researcher is not None:
            self.first_name.errors.append(f'Исследователь {researcher} уже есть в базе данных!')
            return False

        return True

