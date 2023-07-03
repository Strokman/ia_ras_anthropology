from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import DataRequired, NumberRange
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class ArchaeologicalSiteForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.region.choices = [(0, 'Выберите субъект')]

    name = StringField(label='Название памятника', validators=[DataRequiredImproved(), CleanString()])
    long = DecimalField(label='Долгота', validators=[NumberRange(min=-180, max=180, message='KEK'), DataRequiredImproved()])
    lat = DecimalField(label='Широта', validators=[NumberRange(min=-90, max=90), DataRequired()])
    epoch = QuerySelectMultipleField('Эпохи')
    # researcher = SelectField(label='Исследователь', validators=[DataRequiredImproved(), SelectFieldValidator()])
    researcher = QuerySelectField('Исследователи')
    # federal_district = SelectField(label='Федеральный округ', validators=[DataRequiredImproved(), SelectFieldValidator()])
    federal_district = QuerySelectField('Федеральный округ')
    region = NonValidatingSelectField(label='Регион', default='Выберите субъект', validators=[DataRequiredImproved(), SelectFieldValidator()])
    submit = SubmitField('Submit')

