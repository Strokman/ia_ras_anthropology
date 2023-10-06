from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    SubmitField,
    SelectField,
    IntegerField,
    IntegerRangeField,
    TextAreaField
    )
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import NumberRange, Optional, ValidationError

from src.base_habilis.lib.validators import (
    CleanString,
    DataRequiredImproved
    )
from src.repository.models import ArchaeologicalSite, Epoch, Sex


class IndividForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.site.query = ArchaeologicalSite.get_all()
        self.sex.query = Sex.get_all('sex')
        self.type.choices = ['Выберите обряд', 'ингумация', 'кремация']
        self.grave_type.choices = ['Выберите тип', 'курганный', 'грунтовый', 'поселенческий', 'другой']
        self.epoch.query = Epoch.get_all('id')

    site = QuerySelectField('Памятник', allow_blank=True, blank_text='Выберите памятник', validators=[DataRequiredImproved()])

    year = IntegerField(label='Год', validators=[DataRequiredImproved()])
    type = SelectField(label='Обряд', validators=[DataRequiredImproved()])
    age_min = IntegerField(validators=[NumberRange(message='Только число', min=0, max=150), Optional()])
    age_max = IntegerField(validators=[NumberRange(min=0, max=150), Optional()])
    sex = QuerySelectField('Пол', allow_blank=True, blank_text='Выберите пол', validators=[DataRequiredImproved()])
    preservation = IntegerRangeField(label='Сохранность', validators=[NumberRange(min=1, max=4), DataRequiredImproved()])
    epoch = QuerySelectField('Эпоха', allow_blank=True, blank_text='Выберите эпоху', validators=[Optional()])

    grave_type = SelectField(label='Тип памятника', validators=[DataRequiredImproved()])
    kurgan_number = StringField(render_kw={'placeholder': 'номер кургана'}, validators=[CleanString()])
    grave_number = IntegerField(render_kw={'placeholder': 'номер погребения'}, validators=[DataRequiredImproved()])
    catacomb = StringField(render_kw={'placeholder': 'катакомба'} , validators=[CleanString()])
    chamber = StringField(render_kw={'placeholder': 'камера'}, validators=[CleanString()])
    trench = StringField(render_kw={'placeholder': 'раскоп'}, validators=[CleanString()])
    area = StringField(render_kw={'placeholder': 'участок'}, validators=[CleanString()])
    object = StringField(render_kw={'placeholder': 'объект'}, validators=[CleanString()])
    layer = StringField(render_kw={'placeholder': 'слой'}, validators=[CleanString()])
    square = StringField(render_kw={'placeholder': 'квадрат'}, validators=[CleanString()])
    sector = StringField(render_kw={'placeholder': 'сектор'}, validators=[CleanString()])
    niveau_point = StringField(render_kw={'placeholder': 'нив.отметка'}, validators=[CleanString()])
    tachymeter_point = StringField(render_kw={'placeholder': 'тахеом.отметка'}, validators=[CleanString()])
    skeleton = StringField(render_kw={'placeholder': 'скелет'}, validators=[CleanString()])

    comment = TextAreaField(label='Примечание')
    file = FileField(label='Файл: pdf, jpeg', validators=[Optional(), FileAllowed(['pdf', 'jpg', 'jpeg', 'png'], 'Формат файла не поддерживается')])

    submit = SubmitField(label='Добавить индивида')

    def validate_type(self, type):
        if type.data == 'Выберите обряд':
            raise ValidationError('Пожалуйста, выберите один из вариантов')
    
    def validate_grave_type(self, grave_type):
        if grave_type.data == 'Выберите тип':
            raise ValidationError('Пожалуйста, выберите один из вариантов')
