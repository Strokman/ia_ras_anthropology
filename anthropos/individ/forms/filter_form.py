from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from anthropos.models import FederalDistrict, Epoch, Researcher, Sex, Preservation, DatabaseUser, ArchaeologicalSite
from anthropos import db


class FilterForm(FlaskForm):
    class Meta:
        csrf = False

    def __init__(self):
        super().__init__()
        self.federal_district.query = FederalDistrict.get_all(db.session)
        self.researcher.query = Researcher.get_all(db.session, Researcher.last_name)
        self.epoch.query = Epoch.get_all(db.session)
        self.sex.query = Sex.get_all(db.session, Sex.sex)
        self.preservation.query = Preservation.get_all(db.session, Preservation.id)
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий', 'другой']
        self.creator.query = DatabaseUser.get_all(db.session, DatabaseUser.last_name)
        self.site.query = ArchaeologicalSite.get_all(db.session)

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

