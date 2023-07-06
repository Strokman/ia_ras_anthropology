from flask import redirect, url_for, render_template, flash, jsonify, request
from flask_login import login_required, current_user
from anthropos import db
from .forms import IndividForm
from anthropos.individ import bp
from anthropos.models import Grave, Individ, Comment
from datetime import datetime


@bp.route('/submit_individ', methods=['GET', 'POST'])
@login_required
def individ():
    form = IndividForm()
    if form.validate_on_submit():
        grave = Grave(
            type=form.data.get('grave_type', None),
            kurgan_number=form.data.get('kurgan_number', None),
            grave_number=form.data.get('grave_number', None),
            catacomb=form.data.get('catacomb', None),
            chamber=form.data.get('chamber', None),
            trench=form.data.get('trench', None),
            area=form.data.get('area', None),
            object=form.data.get('object', None),
            layer=form.data.get('layer', None),
            square=form.data.get('square', None),
            sector=form.data.get('sector', None),
            niveau_point=form.data.get('niveau_point', None),
            tachymeter_point=form.data.get('tachymeter_point', None),
            skeleton=form.data.get('skeleton', None)
        )
        grave.save_to_db(db.session)
        if site := form.site.data:
            site.graves.append(grave)
        comment = Comment(text=form.comment.data)
        comment.save_to_db(db.session)
        individ = Individ(
            year=form.data.get('year', None),
            age_min=form.data.get('age_min', None),
            age_max=form.data.get('age_max', None),
            site_id=form.data.get('site', None).id,
            preservation_id=form.data.get('preservation', None),
            type=form.data.get('type', None),
            grave_id=grave.id,
            sex_type=form.data.get('sex', None).sex,
            comment_id=comment.id,
            created_at=datetime.utcnow(),
            created_by=current_user.id
        )
        individ.save_to_db(db.session)
        individ.create_index()
        db.session.commit()
        flash('Successfully added', 'success')
        return redirect(url_for('submit.individ'))
    return render_template('individ/submit_individ.html', form=form)