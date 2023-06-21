from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange
from .validators import CleanString


class ArchaeologicalSiteForm(FlaskForm):

    def __init__(self, researchers, regions):
        super().__init__()
        self.researcher.choices = researchers
        self.region.choices = [(region.id, region.name) for region in regions]
        self.federal_district.choices = tuple(set([(region.federal_district.id, region.federal_district.name) for region in regions]))

    name = StringField(label='Name of the site', validators=[DataRequired(), CleanString()])
    long = DecimalField(label='Longitude', validators=[NumberRange(min=-180, max=180), DataRequired()])
    lat = DecimalField(label='Latitude', validators=[NumberRange(min=-90, max=90), DataRequired()])
    researcher = SelectField(label='Исследователь', validators=[DataRequired()])
    federal_district = SelectField(label='Федеральный округ', validators=[DataRequired()])
    region = SelectField(label='Регион', validators=[DataRequired()])
    submit = SubmitField('Submit')

