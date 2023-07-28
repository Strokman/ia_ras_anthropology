from flask import redirect, url_for, render_template, flash
from flask_login import login_required
from anthropos import db
from .forms import ResearcherForm
from anthropos.researcher import bp
from anthropos.models import Researcher
from datetime import datetime


@bp.route('/submit_researcher', methods=['GET', 'POST'])
@login_required
def submit_researcher():
    form = ResearcherForm()
    if form.validate_on_submit():
        researcher = Researcher()
        for k, v in form.data.items():
            if hasattr(researcher, k) and v is not None:
                setattr(researcher, k, v)
        db.session.add(researcher)
        db.session.commit()
        flash('Исследователь добавлен', 'success')
        return redirect(url_for('researcher.submit_researcher'))
    return render_template('researcher/submit_researcher.html', title='Добавление исследователя', form=form)


@bp.route('/researcher_table', methods=['GET', 'POST'])
@login_required
def researcher_table():
    return 'LULKA'