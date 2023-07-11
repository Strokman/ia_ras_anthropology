from flask import redirect, url_for, render_template, flash, jsonify, request
from flask_login import login_required, current_user
from anthropos import db
from .forms import IndividForm
from anthropos.data import bp
from anthropos.models import Grave, Individ, Comment
from datetime import datetime


@bp.route('/individ_data', methods=['GET', 'POST'])
@login_required
def individ_data():
    individs = sorted(Individ.get_all(db.session), key=lambda x: x.index)
    # form = IndividForm()
    return render_template('data_output.html', individs=individs)