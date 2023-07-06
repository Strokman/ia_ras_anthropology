from flask import redirect, url_for, render_template, flash, jsonify, request
from flask_login import login_required, current_user
from anthropos import db
from .forms import IndividForm
from anthropos.submit_data import bp
from anthropos.models import Grave, Individ, Comment
from datetime import datetime


@bp.route('/data', methods=['GET', 'POST'])
@login_required
def data():
    individs = Individ.get_all(db.session)
    form = IndividForm()
    return render_template('data_output.html', individs=individs, form=form)