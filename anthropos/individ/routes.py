from flask import redirect, url_for, render_template, flash, jsonify, send_file, request, current_app, send_from_directory
from flask_login import login_required, current_user
from anthropos import db
from .forms import IndividForm
from anthropos.individ import bp
from anthropos.models import Grave, Individ, Comment, File
from datetime import datetime
from sqlalchemy import select
from os import path, remove
from io import BytesIO

@bp.route('/submit_individ', methods=['GET', 'POST'])
@login_required
def individ():
    form = IndividForm()
    if form.validate_on_submit():
        grave = Grave(
            grave_type=form.data.get('grave_type', None),
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
            sex_type=form.data.get('sex', None).sex,
            created_at=datetime.utcnow(),
            created_by=current_user.id,
            edited_at=datetime.utcnow(),
            edited_by=current_user.id,
        )
        individ.save_to_db(db.session)
        individ.grave = grave
        individ.comment = comment

        individ.create_index()

        
        if file := form.file.data:
            extension = file.filename.rsplit('.', 1)[1].lower()
            if '.' in file.filename and extension in current_app.config['ALLOWED_EXTENSIONS']:
                filename = f'{individ.index}.{extension}'
                saving_path = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
                file.save(saving_path)
            file = File(path=saving_path, filename=filename)
            file.save_to_db(db.session)

            individ.file = file
        form.epoch.data.individ.append(individ)

        db.session.commit()

        flash('Successfully added', 'success')
        return redirect(url_for('individ.individ'))
    return render_template('individ/submit_individ.html', form=form)


@bp.route('/delete_individ/<int:individ_id>', methods=['GET'])
@login_required
def delete_individ(individ_id):
    individ = db.session.scalars(select(Individ).where(Individ.id==individ_id)).first()
    remove(individ.file.path)
    db.session.delete(individ)
    db.session.commit()
    flash('Запись удалена', 'warning')
    return redirect(request.referrer)


@bp.route('/edit_individ/<int:individ_id>', methods=['GET', 'POST'])
@login_required
def edit_individ(individ_id):
    individ = db.session.get(Individ, individ_id)
    form = IndividForm()

    if request.method == 'POST' and form.validate_on_submit():
        individ.grave.grave_type=form.data.get('grave_type', None)
        individ.grave.kurgan_number=form.data.get('kurgan_number', None)
        individ.grave.grave_number=form.data.get('grave_number', None)
        individ.grave.catacomb=form.data.get('catacomb', None)
        individ.grave.chamber=form.data.get('chamber', None)
        individ.grave.trench=form.data.get('trench', None)
        individ.grave.area=form.data.get('area', None)
        individ.grave.object=form.data.get('object', None)
        individ.grave.layer=form.data.get('layer', None)
        individ.grave.square=form.data.get('square', None)
        individ.grave.sector=form.data.get('sector', None)
        individ.grave.niveau_point=form.data.get('niveau_point', None)
        individ.grave.tachymeter_point=form.data.get('tachymeter_point', None)
        individ.grave.skeleton=form.data.get('skeleton', None)
        individ.comment.text = form.comment.data
        individ.year=form.data.get('year', None)
        individ.age_min=form.data.get('age_min', None)
        individ.age_max=form.data.get('age_max', None)
        individ.preservation_id=form.data.get('preservation', None)
        individ.type=form.data.get('type', None)
        individ.edited_at=datetime.utcnow()
        individ.edited_by=current_user.id
        form.sex.data.individ.append(individ)
        if individ.site != (site := form.site.data):
            site.individ.append(individ)
        individ.create_index()
        if file := form.file.data:
            if individ.file != None:
                remove(individ.file.path)
                extension = file.filename.rsplit('.', 1)[1].lower()
                if '.' in file.filename and extension in current_app.config['ALLOWED_EXTENSIONS']:
                    filename = f'{individ.index}.{extension}'
                    save_path = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(save_path)
                    individ.file.path = save_path
                    individ.file.filename = filename
            else:
                extension = file.filename.rsplit('.', 1)[1].lower()
                if '.' in file.filename and extension in current_app.config['ALLOWED_EXTENSIONS']:
                    filename = f'{individ.index}.{extension}'
                    saving_path = path.join(current_app.root_path, current_app.config['UPLOAD_FOLDER'], filename)
                    file.save(saving_path)
                file = File(path=saving_path, filename=filename)
                file.save_to_db(db.session)

                individ.file = file
        if epoch := form.epoch.data:
            epoch.individ.append(individ)
        db.session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(request.referrer)
    elif request.method == 'GET':
        try:
            form.submit.label.text = 'Редактировать'
            form.site.data = individ.site
            form.sex.data = individ.sex
            form.type.data = individ.type
            form.age_min.data = individ.age_min
            form.age_max.data = individ.age_max
            form.year.data = individ.year
            form.preservation.data = individ.preservation.id
            form.epoch.data = individ.epoch
            form.grave_type.data = individ.grave.grave_type
            form.kurgan_number.data = individ.grave.kurgan_number
            form.grave_number.data = individ.grave.grave_number
            form.catacomb.data = individ.grave.catacomb
            form.chamber.data = individ.grave.chamber
            form.trench.data = individ.grave.trench
            form.area.data = individ.grave.area
            form.object.data = individ.grave.object
            form.chamber.data = individ.grave.chamber
            form.layer.data = individ.grave.layer
            form.layer.data = individ.grave.layer
            form.square.data = individ.grave.square
            form.sector.data = individ.grave.sector
            form.niveau_point.data = individ.grave.niveau_point
            form.tachymeter_point.data = individ.grave.tachymeter_point
            form.skeleton.data = individ.grave.skeleton
            form.comment.data = individ.comment.text
        except AttributeError:
            pass
    return render_template('individ/submit_individ.html', form=form)