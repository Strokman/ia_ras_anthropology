from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

from src.base_habilis.lib.validators import (
    CleanName,
    OnlyCharsValidator,
    DataRequiredImproved
    )


class EditResearcherForm(FlaskForm):

    last_name = StringField(label='Фамилия', validators=[DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    first_name = StringField(label='Имя', validators=[DataRequiredImproved(), CleanName(), OnlyCharsValidator()])
    middle_name = StringField(label='Отчество', validators=[CleanName(), OnlyCharsValidator()])
    affiliation = StringField(label='Место работы', validators=[DataRequiredImproved()])
    submit = SubmitField(label='Сохранить изменения')
