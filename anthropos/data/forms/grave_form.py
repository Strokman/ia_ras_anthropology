from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from ...lib.validators import DataRequiredImproved

class GraveForm(FlaskForm):
    def __init__(self):
        super().__init__()
        self.grave_type.choices = ['курганный', 'грунтовый', 'поселенческий', 'другой']


    grave_type = SelectField(label='Тип погребения', validators=[DataRequiredImproved()])
    kurgan_number = StringField(render_kw={'placeholder': 'номер кургана'} )
    grave_number = StringField(render_kw={'placeholder': 'номер погребения'} )
    catacomb = StringField(render_kw={'placeholder': 'катакомба'} )
    chamber = StringField(render_kw={'placeholder': 'камера'})
    trench = StringField(render_kw={'placeholder': 'раскоп'})
    area = StringField(render_kw={'placeholder': 'участок'})
    object = StringField(render_kw={'placeholder': 'объект'})
    layer = StringField(render_kw={'placeholder': 'слой'})
    square = StringField(render_kw={'placeholder': 'квадрат'})
    sector = StringField(render_kw={'placeholder': 'сектор'})
    niveau_point = StringField(render_kw={'placeholder': 'нив.отметка'})
    tachymeter_point = StringField(render_kw={'placeholder': 'тахеом.отметка'})
    skeleton = StringField(render_kw={'placeholder': 'скелет'})

    submit = SubmitField(label='Добавить погребение')