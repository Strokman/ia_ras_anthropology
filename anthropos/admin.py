from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from anthropos.extensions import db
from anthropos.models import (
    ArchaeologicalSite,
    DatabaseUser,
    Region,
    Epoch,
    Individ,
    Preservation,
    Comment,
    FederalDistrict,
    File,
    Grave,
    Researcher,
    Sex
)


admin = Admin(name='BaseHabilis', template_mode='bootstrap4')

admin.add_view(ModelView(DatabaseUser, db.session, name='Users', url='users'))
admin.add_view(ModelView(Individ, db.session, name='Individs', url='individs', endpoint='individs'))
admin.add_view(ModelView(ArchaeologicalSite, db.session, name='Sites'))
admin.add_view(ModelView(Researcher, db.session, endpoint='researchers'))
admin.add_view(ModelView(Grave, db.session))
admin.add_view(ModelView(Comment, db.session))
admin.add_view(ModelView(File, db.session, endpoint='files'))
admin.add_view(ModelView(FederalDistrict, db.session, name='Districts'))
admin.add_view(ModelView(Region, db.session))
admin.add_view(ModelView(Epoch, db.session))
admin.add_view(ModelView(Preservation, db.session))
admin.add_view(ModelView(Sex, db.session))
