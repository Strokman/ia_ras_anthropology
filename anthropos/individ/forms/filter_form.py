from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectMultipleField, SearchField
from wtforms.validators import Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField

from anthropos.models import (
    FederalDistrict,
    Epoch,
    Researcher,
    Sex,
    Preservation,
    DatabaseUser,
    ArchaeologicalSite
    )


class FilterForm(FlaskForm):
    class Meta:
        csrf = False

    def __init__(self):
        super().__init__()
        self.federal_district.query = FederalDistrict.get_all()
        self.researcher.query = Researcher.get_all('last_name')
        self.epoch.query = Epoch.get_all('id')
        self.sex.query = Sex.get_all('sex')
        self.type.choices = ['ингумация', 'кремация']
        self.preservation.query = Preservation.get_all('id')
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий', 'другой']
        self.creator.query = DatabaseUser.get_all('last_name')
        self.site.query = ArchaeologicalSite.get_all()

    index = SearchField('Поиск по индексу', validators=[Optional()])
    site = QuerySelectMultipleField('Памятник')
    epoch = QuerySelectMultipleField('Эпоха')
    year_min = IntegerField(label='Год исследования: от', validators=[Optional()])
    year_max = IntegerField(label='до', validators=[Optional()])
    sex = QuerySelectMultipleField(label='Пол')
    age_min = IntegerField(label='Возраст: от', validators=[Optional()])
    age_max = IntegerField(label='до', validators=[Optional()])
    type = SelectMultipleField(label='Обряд')
    preservation = QuerySelectMultipleField(label='Сохранность')
    grave = IntegerField(label='Номер погребения', validators=[Optional()])
    grave_type = SelectMultipleField(label='Тип погребения')
    researcher = QuerySelectMultipleField('Исследователи')
    federal_district = QuerySelectMultipleField('Федеральный округ')
    comment = SearchField('Поиск по примечанию', validators=[Optional()])
    creator = QuerySelectMultipleField('Кем создан')
    submit = SubmitField('Выбрать')
