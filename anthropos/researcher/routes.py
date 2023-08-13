from flask import redirect, url_for, render_template, flash, request
from flask_login import login_required
from werkzeug.wrappers import Response

from anthropos.models import Researcher
from anthropos.researcher import bp
from anthropos.researcher.forms import ResearcherForm, EditResearcherForm


@bp.route('/researcher_table', methods=['GET', 'POST'])
@login_required
def researcher_table() -> str:
    """
    researcher_table load all entries from researchers table
    and render a table with existing data

    Returns:
        str: Template with the table of researchers
    """
    researchers: list[tuple[int, Researcher]] = enumerate(Researcher.get_all('last_name'), 1)
    return render_template('researcher/researcher_table.html', title='Таблица исследователей', researchers=researchers)


@bp.route('/submit_researcher', methods=['GET', 'POST'])
@login_required
def submit_researcher() -> Response | str:
    form = ResearcherForm()
    if form.validate_on_submit():
        researcher: Researcher = Researcher.create(**form.data)
        flash(f'Исследователь {researcher} добавлен', 'success')
        return redirect(url_for('researcher.submit_researcher'))
    return render_template('researcher/submit_researcher.html', title='Добавление исследователя', form=form)


@bp.route('/edit_researcher/<int:researcher_id>', methods=['GET', 'POST'])
@login_required
def edit_researcher(researcher_id: int) -> Response | str:
    """
    edit_researcher - endpoint takes an id of the researcher as argument,
    loads the researcher by this id, and updates it if any changes were made.

    Args:
        researcher_id (int): id of the researcher to edit.

    Returns:
        Response | str:
        POST - redirects the user to the researcher table output
        GET - renders edit researcher form prepopulated with existing data.
    """
    researcher: Researcher | None = Researcher.get_by_id(researcher_id)
    form = EditResearcherForm()
    if request.method == 'POST' and form.validate_on_submit():
        """If form is submitted and validated - update record in the database"""
        researcher.update(**form.data)
        flash('Изменения сохранены', 'success')
        return redirect(url_for('researcher.researcher_table'))
    elif request.method == 'GET':
        # populate the form with existing data from DB
        form.last_name.data = researcher.last_name
        form.first_name.data = researcher.first_name
        form.middle_name.data = researcher.middle_name
        form.affiliation.data = researcher.affiliation
        form.submit.label.text = 'Редактировать'
    return render_template('researcher/submit_researcher.html', title='Редактировать исследователя', form=form)
