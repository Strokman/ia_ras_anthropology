from wtforms.validators import ValidationError


class CleanString(object):
    def __call__(self, form, field):
        if field.data == '':
            field.data = None
            return field.data
        field.data = field.data.replace('.', '').strip().lower().capitalize()
        return field.data


class SelectFieldValidator(object):
    def __call__(self, form, field):
        if int(field.data) == 0:
            raise ValidationError('Пожалуйста, выберите из выпадающего списка')


class OnlyCharsValidator(object):
    def __call__(self, form, field):
        data: str = field.data
        if not data.isalpha():
            raise ValidationError('Допускаются только буквы')