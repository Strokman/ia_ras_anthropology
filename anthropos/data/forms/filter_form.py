from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange, Length
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from anthropos.models import FederalDistrict, Epoch, Researcher
from anthropos import db

class FilterForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.federal_district.query = sorted(FederalDistrict.get_all(db.session), key=lambda x: x.name)
        self.researcher.query = sorted(Researcher.get_all(db.session), key=lambda x: x.last_name)
        self.epoch.query = Epoch.get_all(db.session)

    epoch = QuerySelectMultipleField('Эпохи')
    year_min = IntegerField(label='Год исследования: от')
    year_max = IntegerField(label='до')
    researcher = QuerySelectField('Исследователи', allow_blank=True, blank_text='Выберите исследователя')
    federal_district = QuerySelectField('Федеральный округ', allow_blank=True, blank_text='Выберите округ')
    submit = SubmitField('Выбрать')

