from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_session import Session
from flask_mail import Mail


db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Пожалуйста, войдите в учетную запись'
login.login_message_category = "info"
admin = Admin(name='BaseHabilis', template_mode='bootstrap4')
sess = Session()
mail = Mail()