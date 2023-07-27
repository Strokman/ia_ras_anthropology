from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, IntegerField, SelectMultipleField
from wtforms.validators import Optional
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from anthropos.models import FederalDistrict, Epoch, Researcher, Sex, Preservation, DatabaseUser, ArchaeologicalSite
from anthropos import db
from anthropos.site.forms import NonValidatingSelectField


class FilterForm(FlaskForm):
    class Meta:
        csrf = False

    def __init__(self):
        super().__init__()
        self.federal_district.query = sorted(FederalDistrict.get_all(db.session), key=lambda x: x.name)
        self.researcher.query = sorted(Researcher.get_all(db.session), key=lambda x: x.last_name)
        self.epoch.query = Epoch.get_all(db.session)
        self.sex.query = Sex.get_all(db.session)
        self.preservation.query = Preservation.get_all(db.session)
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий', 'другой']
        self.creator.query = sorted(DatabaseUser.get_all(db.session), key=lambda x: x.last_name)
        self.site.query = sorted(ArchaeologicalSite.get_all(db.session), key=lambda x: x.name)

    site = QuerySelectMultipleField('Памятник')
    epoch = QuerySelectMultipleField('Эпоха')
    year_min = IntegerField(label='Год исследования: от', validators=[Optional()])
    year_max = IntegerField(label='до', validators=[Optional()])
    sex = QuerySelectMultipleField(label='Пол')
    # age_min = IntegerField(label='Возраст: от', validators=[Optional()])
    # age_max = IntegerField(label='до', validators=[Optional()])
    preservation = QuerySelectMultipleField(label='Сохранность')
    grave_type = SelectMultipleField(label='Тип погребения')
    researcher = QuerySelectMultipleField('Исследователи')
    federal_district = QuerySelectMultipleField('Федеральный округ')
    creator = QuerySelectMultipleField('Кем создан')
    submit = SubmitField('Выбрать')

