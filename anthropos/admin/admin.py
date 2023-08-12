from flask_admin import Admin
from flask_admin.contrib.fileadmin import FileAdmin

from anthropos.admin.models import MyAdminView, MyModelView, UserView
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


admin = Admin(name='BaseHabilis Admin',
              base_template='admin/master.html',
              template_mode='bootstrap4',
              index_view=MyAdminView())

admin.add_view(UserView(DatabaseUser, db.session, name='Users', url='users'))
admin.add_view(MyModelView(Individ, db.session, name='Individs', url='individs', endpoint='individs'))
admin.add_view(MyModelView(ArchaeologicalSite, db.session, name='Sites'))
admin.add_view(MyModelView(Researcher, db.session, endpoint='researchers'))
admin.add_view(MyModelView(Grave, db.session))
admin.add_view(MyModelView(Comment, db.session))
admin.add_view(MyModelView(File, db.session, endpoint='files'))
admin.add_view(MyModelView(FederalDistrict, db.session, category='Locations'))
admin.add_view(MyModelView(Region, db.session, category='Locations'))
admin.add_view(MyModelView(Epoch, db.session, category='Fixed tables'))
admin.add_view(MyModelView(Preservation, db.session, category='Fixed tables'))
admin.add_view(MyModelView(Sex, db.session, category='Fixed tables'))
admin.add_view(FileAdmin('anthropos/static', '/static/', name='Static Files'))
