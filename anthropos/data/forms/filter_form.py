from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import DataRequired, NumberRange, Length
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from anthropos.models import FederalDistrict, Epoch, Researcher, Sex, Preservation
from anthropos import db
from anthropos.site.forms import NonValidatingSelectField


class FilterForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.federal_district.query = sorted(FederalDistrict.get_all(db.session), key=lambda x: x.name)
        self.researcher.query = sorted(Researcher.get_all(db.session), key=lambda x: x.last_name)
        self.epoch.query = Epoch.get_all(db.session)
        self.sex.query = Sex.get_all(db.session)
        self.preservation.query = Preservation.get_all(db.session)
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий', 'другой']

    epoch = QuerySelectMultipleField('Эпохи')
    year_min = IntegerField(label='Год исследования: от')
    year_max = IntegerField(label='до')
    sex = QuerySelectMultipleField(label='Пол')
    preservation = QuerySelectMultipleField(label='Сохранность')
    grave_type = SelectMultipleField(label='Тип погребения')
    researcher = QuerySelectMultipleField('Исследователи')
    federal_district = QuerySelectField('Федеральный округ', allow_blank=True, blank_text='Выберите округ')
    submit = SubmitField('Выбрать')

