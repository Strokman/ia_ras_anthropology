from flask import redirect, url_for, render_template, flash, request
from flask_login import login_required
from anthropos import db
from .forms import ResearcherForm
from anthropos.researcher import bp
from anthropos.models import Researcher


@bp.route('/submit_researcher', methods=['GET', 'POST'])
@login_required
def submit_researcher():
    form = ResearcherForm(url_for('researcher.submit_researcher'))
    if form.validate_on_submit():
        researcher = Researcher()
        for key, value in form.data.items():
            if hasattr(researcher, key) and value is not None:
                setattr(researcher, key, value)
        db.session.add(researcher)
        db.session.commit()
        flash('Исследователь добавлен', 'success')
        return redirect(url_for('researcher.submit_researcher'))
    return render_template('researcher/submit_researcher.html', title='Добавление исследователя', form=form)


@bp.route('/researcher_table', methods=['GET', 'POST'])
@login_required
def researcher_table():
    researchers = enumerate(Researcher.get_all(Researcher.last_name), 1)
    return render_template('researcher/researcher_table.html', title='Таблица исследователей', researchers=researchers)

@bp.route('/edit_researcher/<researcher_id>', methods=['GET', 'POST'])
@login_required
def edit_researcher(researcher_id):
    researcher = db.session.get(Researcher, researcher_id)
    form = ResearcherForm()
    if request.method == 'POST' and form.validate_on_submit():
        researcher.last_name = form.last_name.data
        researcher.first_name = form.first_name.data
        researcher.middle_name = form.middle_name.data
        researcher.affiliation = form.affiliation.data
        db.session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('researcher.researcher_table'))
    elif request.method == 'GET':
        form.last_name.data = researcher.last_name
        form.first_name.data = researcher.first_name
        form.middle_name.data = researcher.middle_name
        form.affiliation.data = researcher.affiliation
        form.submit.label.text = 'Редактировать'
    return render_template('researcher/submit_researcher.html', title='Редактировать исследователя', form=form)