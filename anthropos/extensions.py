from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please login to access this page'
login.login_message_category = "info"
admin = Admin(name='BaseHabilis', template_mode='bootstrap4')
# admin.add_view(ModelView(ArchaeologicalSite, db.session))
sess = Session()