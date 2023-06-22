from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange
from .validators import CleanString, SelectFieldValidator


class ArchaeologicalSiteForm(FlaskForm):

    def __init__(self, researchers, fed_districts):
        super().__init__()
        self.researcher.choices = researchers
        self.region.choices = [(0, 'Выберите субъект')]
        self.federal_district.choices = fed_districts

    name = StringField(label='Название памятника', validators=[DataRequired(), CleanString()])
    long = DecimalField(label='Долгота', validators=[NumberRange(min=-180, max=180), DataRequired()])
    lat = DecimalField(label='Широта', validators=[NumberRange(min=-90, max=90), DataRequired()])
    researcher = SelectField(label='Исследователь', validators=[DataRequired(), SelectFieldValidator()])
    federal_district = SelectField(label='Федеральный округ', validators=[DataRequired(), SelectFieldValidator()])
    region = SelectField(label='Регион', default='Выберите субъект', validators=[DataRequired(), SelectFieldValidator()])
    submit = SubmitField('Submit')

