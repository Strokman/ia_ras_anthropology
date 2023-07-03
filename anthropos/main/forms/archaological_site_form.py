from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange
from .validators import CleanString, SelectFieldValidator, DataRequiredImproved


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class ArchaeologicalSiteForm(FlaskForm):

    def __init__(self, researchers, fed_districts, epochs):
        super().__init__()
        self.researcher.choices = researchers
        self.region.choices = [(0, 'Выберите субъект')]
        self.epoch.choices = epochs
        self.federal_district.choices = fed_districts

    name = StringField(label='Название памятника', validators=[DataRequiredImproved(), CleanString()])
    long = DecimalField(label='Долгота', validators=[NumberRange(min=-180, max=180, message='KEK'), DataRequiredImproved()])
    lat = DecimalField(label='Широта', validators=[NumberRange(min=-90, max=90), DataRequired()])
    researcher = SelectField(label='Исследователь', validators=[DataRequiredImproved(), SelectFieldValidator()])
    federal_district = SelectField(label='Федеральный округ', validators=[DataRequiredImproved(), SelectFieldValidator()])
    epoch = SelectField(label='Эпоха', validators=[DataRequiredImproved(), SelectFieldValidator()])
    region = NonValidatingSelectField(label='Регион', default='Выберите субъект', validators=[DataRequiredImproved(), SelectFieldValidator()])
    submit = SubmitField('Submit')

