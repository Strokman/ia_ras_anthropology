"""
    Admin module of Base Habilis app instanciates
    the flask_admin class and adds necessary views to
    admin panel of the application.
    Recent customization is pretty basic.
"""
from flask_admin import Admin

from src.base_habilis.admin.models import MyAdminView, MyModelView, UserView
from src.repository import session
from src.repository.models import (
    ArchaeologicalSite,
    User,
    Region,
    Epoch,
    Individ,
    Preservation,
    Country,
    File,
    Grave,
    Researcher,
    Sex
)

admin = Admin(name='BaseHabilis Admin',
              base_template='admin/master.html',
              template_mode='bootstrap4',
              index_view=MyAdminView(name='BaseHabilis Admin'))

admin.add_view(UserView(User, session, name='Users', url='users', endpoint='users'))
admin.add_view(MyModelView(Individ, session, name='Individs', url='individs', endpoint='individs'))
admin.add_view(MyModelView(ArchaeologicalSite, session, name='Sites'))
admin.add_view(MyModelView(Researcher, session, endpoint='researchers'))
admin.add_view(MyModelView(Grave, session))
admin.add_view(MyModelView(File, session, endpoint='files'))
admin.add_view(MyModelView(Country, session, category='Locations'))
admin.add_view(MyModelView(Region, session, category='Locations'))
admin.add_view(MyModelView(Epoch, session, category='Fixed tables'))
admin.add_view(MyModelView(Preservation, session, category='Fixed tables'))
admin.add_view(MyModelView(Sex, session, category='Fixed tables'))
