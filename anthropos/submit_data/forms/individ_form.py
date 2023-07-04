from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, IntegerField, IntegerRangeField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, NumberRange
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved
from anthropos.models import ArchaeologicalSite, Sex, Researcher
from anthropos import db

class IndividForm(FlaskForm):

    def __init__(self):
        super().__init__()
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий', 'другой']
        self.site.query = ArchaeologicalSite.get_all(db.session)
        self.sex.query = Sex.get_all(db.session)
        self.type.choices = ['ингумация', 'кремация']
        # self.researcher.query = Researcher.get_all(db.session)

    site = QuerySelectField('Памятник', allow_blank=True, blank_text='Выберите памятник', validators=[DataRequiredImproved()])
    # researcher = QuerySelectField('Исследователь', allow_blank=True, blank_text='Выберите исследователя', validators=[DataRequiredImproved()])
    
    year = IntegerField(label='Год')
    type = SelectField(label='Обряд')
    age_min = IntegerField(label='Возраст мин')
    age_max = IntegerField(label='Возраст макс')
    sex = QuerySelectField('Пол', allow_blank=True, blank_text='Выберите пол')
    preservation = IntegerRangeField(label='Сохранность', validators=[NumberRange(min=1, max=4), DataRequiredImproved()])

    grave_type = SelectField(label='Тип погребения', validators=[DataRequiredImproved()])
    kurgan_number = StringField(render_kw={'placeholder': 'номер кургана'} )
    grave_number = StringField(render_kw={'placeholder': 'номер погребения'} )
    catacomb = StringField(render_kw={'placeholder': 'катакомба'} )
    chamber = StringField(render_kw={'placeholder': 'камера'})
    trench = StringField(render_kw={'placeholder': 'раскоп'})
    area = StringField(render_kw={'placeholder': 'участок'})
    object = StringField(render_kw={'placeholder': 'объект'})
    layer = StringField(render_kw={'placeholder': 'слой'})
    plast = StringField(render_kw={'placeholder': 'пласт'})
    horizont = StringField(render_kw={'placeholder': 'горизонт'})
    square = StringField(render_kw={'placeholder': 'квадрат'})
    sector = StringField(render_kw={'placeholder': 'сектор'})
    niveau_point = StringField(render_kw={'placeholder': 'нив.отметка'})
    tachymeter_point = StringField(render_kw={'placeholder': 'тахеом.отметка'})
    skeleton = StringField(render_kw={'placeholder': 'скелет'})

    comment = StringField(label='Примечание')
    submit = SubmitField(label='Добавить данные')