from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from anthropos.models import FederalDistrict, Epoch, Researcher
from anthropos import db


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class ArchaeologicalSiteForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.region.choices = [(0, 'Выберите субъект')]
        self.federal_district.query = FederalDistrict.get_all(db.session, FederalDistrict.id)
        self.researcher.query = Researcher.get_all(db.session, Researcher.last_name)
        self.epoch.query = Epoch.get_all(db.session, Epoch.id)

    name = StringField(label='Название памятника', validators=[Length(min=4, message='Длина названия не менее 4 знаков'), DataRequiredImproved(), CleanString()])
    long = DecimalField(places=6, label='Долгота', validators=[NumberRange(min=-180, max=180, message='Градусы должны быть в пределах -180 - 180'), DataRequiredImproved()])
    lat = DecimalField(places=6, label='Широта', validators=[NumberRange(min=-90, max=90), DataRequired()])
    epoch = QuerySelectMultipleField('Эпохи')
    researcher = QuerySelectField('Исследователи', allow_blank=True, blank_text='Выберите исследователя', validators=[DataRequiredImproved()])
    federal_district = QuerySelectField('Федеральный округ', allow_blank=True, blank_text='Выберите округ', validators=[DataRequiredImproved()])
    region = NonValidatingSelectField(label='Регион', default='Выберите субъект', validators=[DataRequiredImproved(), SelectFieldValidator()])
    submit = SubmitField('Добавить памятник')

