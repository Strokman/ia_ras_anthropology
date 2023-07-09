from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import StringField, SubmitField, SelectField, IntegerField, IntegerRangeField, TextAreaField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from anthropos.models import ArchaeologicalSite, Sex, Researcher
from anthropos import db

class IndividForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.site.query = ArchaeologicalSite.get_all(db.session)
        self.sex.query = Sex.get_all(db.session)
        self.type.choices = ['ингумация', 'кремация']
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий', 'другой']

    site = QuerySelectField('Памятник', allow_blank=True, blank_text='Выберите памятник', validators=[DataRequiredImproved()])
    
    year = IntegerField(label='Год')
    type = SelectField(label='Обряд')
    age_min = IntegerField(label='Возраст мин', validators=[NumberRange(min=0, max=150)])
    age_max = IntegerField(label='Возраст макс', validators=[NumberRange(min=0, max=150)])
    sex = QuerySelectField('Пол', allow_blank=True, blank_text='Выберите пол', validators=[DataRequiredImproved()])
    preservation = IntegerRangeField(label='Сохранность', validators=[NumberRange(min=1, max=4), DataRequiredImproved()])
    
    grave_type = SelectField(label='Тип погребения', validators=[DataRequiredImproved()])
    kurgan_number = StringField(render_kw={'placeholder': 'номер кургана'}, validators=[CleanString()])
    grave_number = StringField(render_kw={'placeholder': 'номер погребения'} , validators=[CleanString()])
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
    file = FileField(label='Файл')

    submit = SubmitField(label='Добавить индивида')