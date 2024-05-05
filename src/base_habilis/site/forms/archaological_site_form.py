from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import StringField, SubmitField, DecimalField, SelectField
from wtforms.validators import NumberRange, Length, Optional
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
from src.repository.models import Epoch, Researcher


class NonValidatingSelectField(SelectField):
    def pre_validate(self, form):
        pass


class ArchaeologicalSiteForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.researcher.query = Researcher.get_all('last_name')
        self.epoch.query = Epoch.get_all('id')

    name = StringField(label='Название памятника', validators=[Length(min=4, message='Длина названия не менее 4 знаков'), DataRequiredImproved(), CleanString()])
    lat = DecimalField(places=6, label='Широта', validators=[NumberRange(min=-90, max=90, message='Градусы должны быть в пределах -90 - 90'), DataRequiredImproved()])
    long = DecimalField(places=6, label='Долгота', validators=[NumberRange(min=-180, max=180, message='Градусы должны быть в пределах -180 - 180'), DataRequiredImproved()])
    epoch = QuerySelectMultipleField('Эпохи', validators=[Optional()])
    researcher = QuerySelectField('Исследователи', allow_blank=True, blank_text='Выберите исследователя', validators=[DataRequiredImproved()]) # if possibility of multiple selection will be added - just convert to QuerySelectMultipleField and remove blank option
    file = FileField(label='Файл с доп. информацией: pdf, xls, doc', validators=[Optional(), FileAllowed(['xls', 'xlsx', 'doc', 'pdf'], 'Формат файла не поддерживается')])
    submit = SubmitField('Добавить памятник')
