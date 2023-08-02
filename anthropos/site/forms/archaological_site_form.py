from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange, Length
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from anthropos.models import FederalDistrict, Epoch, Researcher


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class ArchaeologicalSiteForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.region.choices = [(0, 'Выберите субъект')]
        self.federal_district.query = FederalDistrict.get_all(FederalDistrict.id)
        self.researcher.query = Researcher.get_all(Researcher.last_name)
        self.epoch.query = Epoch.get_all(Epoch.id)

    name = StringField(label='Название памятника', validators=[Length(min=4, message='Длина названия не менее 4 знаков'), DataRequiredImproved(), CleanString()])
    lat = DecimalField(places=6, label='Широта', validators=[NumberRange(min=-90, max=90), DataRequired()])
    long = DecimalField(places=6, label='Долгота', validators=[NumberRange(min=-180, max=180, message='Градусы должны быть в пределах -180 - 180'), DataRequiredImproved()])
    epoch = QuerySelectMultipleField('Эпохи')
    researcher = QuerySelectMultipleField('Исследователи', validators=[DataRequiredImproved()])
    federal_district = QuerySelectField('Федеральный округ', allow_blank=True, blank_text='Выберите округ', validators=[DataRequiredImproved()])
    region = NonValidatingSelectField(label='Регион', default='Выберите субъект', validators=[DataRequiredImproved(), SelectFieldValidator()])
    submit = SubmitField('Добавить памятник')

