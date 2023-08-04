from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from anthropos.extensions import db
from anthropos.models import (
    ArchaeologicalSite,
    DatabaseUser,
    Region,
    Epoch
)


admin = Admin(name='BaseHabilis', template_mode='bootstrap4')

admin.add_view(ModelView(DatabaseUser, db.session))
admin.add_view(ModelView(ArchaeologicalSite, db.session))
admin.add_view(ModelView(Region, db.session))
admin.add_view(ModelView(Epoch, db.session))