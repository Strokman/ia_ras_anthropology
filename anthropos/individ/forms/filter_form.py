from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectMultipleField
from wtforms.validators import Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from anthropos.models import FederalDistrict, Epoch, Researcher, Sex, Preservation, DatabaseUser, ArchaeologicalSite


class FilterForm(FlaskForm):
    class Meta:
        csrf = False

    def __init__(self):
        super().__init__()
        self.federal_district.query = FederalDistrict.get_all()
        self.researcher.query = Researcher.get_all(Researcher.last_name)
        self.epoch.query = Epoch.get_all()
        self.sex.query = Sex.get_all(Sex.sex)
        self.type.choices = ['ингумация', 'кремация']
        self.preservation.query = Preservation.get_all(Preservation.id)
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий', 'другой']
        self.creator.query = DatabaseUser.get_all(DatabaseUser.last_name)
        self.site.query = ArchaeologicalSite.get_all()

    site = QuerySelectMultipleField('Памятник')
    epoch = QuerySelectMultipleField('Эпоха')
    year_min = IntegerField(label='Год исследования: от', validators=[Optional()])
    year_max = IntegerField(label='до', validators=[Optional()])
    sex = QuerySelectMultipleField(label='Пол')
    type = SelectMultipleField(label='Обряд')
    # age_min = IntegerField(label='Возраст: от', validators=[Optional()])
    # age_max = IntegerField(label='до', validators=[Optional()])
    preservation = QuerySelectMultipleField(label='Сохранность')
    grave_type = SelectMultipleField(label='Тип погребения')
    researcher = QuerySelectMultipleField('Исследователи')
    federal_district = QuerySelectMultipleField('Федеральный округ')
    creator = QuerySelectMultipleField('Кем создан')
    submit = SubmitField('Выбрать')

