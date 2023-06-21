class CleanString(object):
    def __call__(self, form, field):
        field.data = field.data.replace('.', '').strip().lower().capitalize()
        return field.data