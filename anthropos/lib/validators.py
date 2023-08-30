from wtforms.validators import ValidationError, DataRequired
from werkzeug.utils import secure_filename
from flask import current_app


class DataRequiredImproved(DataRequired):
    def __init__(self):
        super().__init__()
        self.message = 'Пожалуйста, заполните данное поле'


class CleanString(object):
    def __call__(self, form, field):
        if field.data and '@' in field.data:
            raise ValidationError('Адрес электронной почты не должен быть именем пользователя')
        try:
            if field.data == '':
                field.data = None
                return field.data
            elif field.data == None:
                return   
            field.data = field.data.replace('.', '').replace('/', '-').replace('\\', '-').strip()
            return field.data
        except:
            pass

class CleanName(object):
    def __call__(self, form, field):
        try:
            if field.data == '':
                field.data = None
                return field.data
            elif field.data == None:
                return   
            field.data = field.data.replace('.', '').replace('/', '-').replace('\\', '-').strip().lower().capitalize()
            return field.data
        except:
            pass


class FileFieldValidator(object):
    def __call__(self, form, field):
        filename = secure_filename(field.data.filename)
        if '.' not in filename:
            raise ValidationError('Некорректное имя файла: отсутствует расширение')
        elif filename.rsplit('.', 1)[1].lower() not in current_app.config['ALLOWED_EXTENSIONS']:
            raise ValidationError('Формат файла не поддерживается')


class SelectFieldValidator(object):
    def __call__(self, form, field):
        if int(field.data) == 0:
            raise ValidationError('Пожалуйста, выберите из выпадающего списка')



class OnlyCharsValidator(object):
    def __call__(self, form, field):
        if not field.data:
            return field.data
        if not field.data.isalpha():
            raise ValidationError('Допускаются только буквы')
        