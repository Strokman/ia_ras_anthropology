from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, SelectField, IntegerField, IntegerRangeField
from wtforms.widgets import RangeInput
from wtforms.validators import DataRequired, NumberRange
from ...lib.validators import CleanString, SelectFieldValidator, DataRequiredImproved