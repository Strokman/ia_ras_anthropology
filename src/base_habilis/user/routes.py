from flask import flash, redirect, render_template, url_for
from flask import session as sess
from flask_login import current_user, login_required
from werkzeug.wrappers import Response

from sqlalchemy import select, desc

from src.repository import session
from src.base_habilis.user import bp
from src.repository.models import User, Individ
from src.base_habilis.user.forms import EditProfileForm
from src.core.models import IndividCore
from src.repository.models.user import owner_required

@bp.route('/user/<username>', methods=['GET'])
@owner_required
@login_required
def user(username) -> str:
    user = User.get_one_by_attr('username', session, username)
    profile_form = EditProfileForm(current_user.username, current_user.email)
    profile_form.username.data = current_user.username
    profile_form.first_name.data = current_user.first_name
    profile_form.last_name.data = current_user.last_name
    profile_form.middle_name.data = current_user.middle_name
    profile_form.affiliation.data = current_user.affiliation
    profile_form.email.data = current_user.email
    stmt = select(Individ).filter_by(created_by=user.id).order_by(desc(Individ.created_at))
    individs = session.execute(stmt).scalars().all()
    key = user.username
    sess.pop(key, None)
    to_save = [IndividCore.model_validate(individ) for individ in individs]
    sess[key] = to_save
    return render_template('user/profile.html',
                           user=user,
                           profile_form=profile_form,
                           individs=individs,
                           key=key)


@bp.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile() -> Response:
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.middle_name = form.middle_name.data
        current_user.affiliation = form.affiliation.data
        if form.email.data != current_user.email:
            current_user.email = form.email.data
            current_user.activated = False
            current_user.send_confirmation_email()
        session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('user.user', username=current_user.username))
    flash('Изменения не сохранены. См. ошибки ниже', 'danger')
    for field in form:
        if field.errors:
            flash(f'Поле {field.label.text} - {field.errors[0]}', 'warning')
    return redirect(url_for('user.user', username=current_user.username))
