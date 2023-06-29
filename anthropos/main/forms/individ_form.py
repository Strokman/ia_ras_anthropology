from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, IntegerField, IntegerRangeField
from wtforms.widgets import RangeInput
from wtforms.validators import DataRequired, NumberRange
from .validators import CleanString, SelectFieldValidator, DataRequiredImproved


class IndividForm(FlaskForm):

    def __init__(self, sex, sites):
        super().__init__()
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий']
        self.site.choices = sites
        self.sex.choices = sex
        self.type.choices = ['ингумация', 'кремация']

    site = SelectField(label='Памятник', validators=[DataRequiredImproved(), SelectFieldValidator()])
    grave_type = SelectField(label='Тип погребения', validators=[DataRequiredImproved()])
    type = SelectField(label='Обряд')
    year = IntegerField(label='Год')
    grave_number = IntegerField(label='Номер погребения')
    preservation = IntegerRangeField(label='Сохранность', validators=[NumberRange(min=1, max=4), DataRequiredImproved()])
    age_min = IntegerField(label='Возраст мин')
    age_max = IntegerField(label='Возраст макс')
    sex = SelectField(label='Пол', validators=[DataRequiredImproved()])
    comment = StringField(label='Примечание')
    submit = SubmitField(label='Добавить данные')