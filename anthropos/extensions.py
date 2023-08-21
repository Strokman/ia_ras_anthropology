from flask_bootstrap import Bootstrap5
from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment
from flask_session import Session
# from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect


bootstrap = Bootstrap5()
cache = Cache()
csrf = CSRFProtect()
# db = SQLAlchemy()

login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Пожалуйста, войдите в учетную запись'
login.login_message_category = "info"

mail = Mail()
migrate = Migrate()
moment = Moment()
sess = Session()
