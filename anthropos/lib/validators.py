from wtforms.validators import ValidationError, DataRequired


class DataRequiredImproved(DataRequired):
    def __init__(self):
        super().__init__()
        self.message = 'Пожалуйста, заполните данное поле'


class CleanString(object):
    def __call__(self, form, field):
        try:
            if field.data == '':
                field.data = None
                return field.data
            elif field.data == None:
                return   
            field.data = field.data.replace('.', '').strip().lower().capitalize()
            return field.data
        except:
            print(form)
            print(field)
            print(field.data)


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