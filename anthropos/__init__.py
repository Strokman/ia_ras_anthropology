from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from flask_admin import Admin


app = Flask(__name__)
mail = Mail(app)
app.config.from_object(Config)

admin = Admin(app, name='strokoff', template_mode='bootstrap3')


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)
login.login_view = 'login'



from anthropos import routes
