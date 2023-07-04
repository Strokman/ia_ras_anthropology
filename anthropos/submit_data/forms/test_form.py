from wtforms_sqlalchemy.orm import model_form
from anthropos.models import Grave
from flask_wtf import FlaskForm

GraveForm = model_form(Grave, base_class=FlaskForm)