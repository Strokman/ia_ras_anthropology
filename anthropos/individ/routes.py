from flask import redirect, url_for, render_template, flash, request, current_app, session
from flask_login import login_required, current_user
from anthropos import db, cache
from .forms import IndividForm
from anthropos.individ import bp
from datetime import datetime
from sqlalchemy import select, or_, between, and_, case
from os import remove
from .forms import FilterForm
from anthropos.models import Sex, Individ, Researcher, ArchaeologicalSite, Epoch, FederalDistrict, Region, Preservation, Grave, DatabaseUser, Comment, File
from anthropos.helpers import save_file


@bp.route('/submit_individ', methods=['GET', 'POST'])
@login_required
def submit_individ():
    form = IndividForm()
    if form.validate_on_submit():

        # If form submitted correctly
        # create instance of Individ class
        individ = Individ(
            year=form.data.get('year', None),
            age_min=form.data.get('age_min', None),
            age_max=form.data.get('age_max', None),
            site_id=form.data.get('site', None).id,
            preservation_id=form.data.get('preservation', None),
            type=form.data.get('type', None),
            created_at=datetime.utcnow(),
            created_by=current_user.id,
            edited_at=datetime.utcnow(),
            edited_by=current_user.id,
        )

        # create instance of Grave class
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

        # add both to the session, so that everything will work correct with ID's etc.
        db.session.add_all((individ, grave))
        
        # add requiered relations
        individ.grave = grave
        sex = form.sex.data
        sex.individs.append(individ)
        site = form.site.data
        site.graves.append(grave)
        site.individs.append(individ)

        # create index of individ - because it requieres grave it is only here, \
        # after grave is initialized and related to the individ
        individ.create_index()

        # check if file, comment and epoch were submitted, than instanciate everything,\
        #  add to the session create relations
        if form.comment.data:
            comment = Comment(text=form.comment.data)
            db.session.add(comment)
            individ.comment = comment

        if epoch := form.epoch.data:
            epoch.individ.append(individ)

        if uploaded_file := form.file.data:
            saved_file = save_file(uploaded_file, current_app)
            file = File(path=saved_file.get('path'), filename=saved_file.get('filename'), extension=saved_file.get('extension'))
            db.session.add(file)
            individ.file = file

        # commit all changes to the DB
        db.session.commit()

        flash('Успешно добавлено', 'success')
        return redirect(url_for('individ.submit_individ'))
    return render_template('individ/submit_individ.html', form=form)


@bp.route('/delete_individ/<int:individ_id>', methods=['GET'])
@login_required
def delete_individ(individ_id):
    individ = db.session.scalars(select(Individ).where(Individ.id==individ_id)).first()
    try:
        remove(individ.file.path)
    except AttributeError as e:
        print(e)
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
        individ.year=form.data.get('year', None)
        individ.age_min=form.data.get('age_min', None)
        individ.age_max=form.data.get('age_max', None)
        individ.preservation_id=form.data.get('preservation', None) # ПРОВЕРИТЬ
        individ.type=form.data.get('type', None)
        individ.edited_at=datetime.utcnow()
        individ.edited_by=current_user.id
        
        sex = form.sex.data
        sex.individs.append(individ)
        
        if input_comment := form.comment.data:
            comment = Comment(text=input_comment)
            db.session.add(comment)
            individ.comment = comment
        if individ.site != (site := form.site.data):
            site.individ.append(individ)
        individ.create_index()
        if uploaded_file := form.file.data:
            if individ.file != None:
                remove(individ.file.path)
                saved_file = save_file(uploaded_file, current_app)
                individ.file.path = saved_file.get('path')
                individ.file.filename = saved_file.get('filename')
                individ.file.extension = saved_file.get('extension')
            else:
                saved_file = save_file(uploaded_file, current_app)
                file = File(path=saved_file.get('path'), filename=saved_file.get('filename'), extension=saved_file.get('extension'))
                db.session.add(file)
                individ.file = file
        if epoch := form.epoch.data:
            epoch.individ.append(individ)
        db.session.commit()
        flash('Изменения сохранены', 'success')
        return redirect(url_for('individ.individ_table'))
    elif request.method == 'GET':
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
        if individ.comment:
            form.comment.data = individ.comment.text
    return render_template('individ/submit_individ.html', form=form)


@bp.route('/individ_table', methods=['GET'])
@login_required
def individ_table():
    individs: list[Individ] = Individ.get_all(Individ.index)
    key = 'all'
    session.pop(key, None)
    session.setdefault(key, individs)
    form: FilterForm = FilterForm()
    return render_template('individ/individ_table.html',
                           title='Таблица индивидов',
                           individs=enumerate(individs, 1),
                           form=form,
                           key=key,
                           action=url_for('individ.individ_table'))


@bp.route('/individ_filter', methods=['GET'])
@login_required
def search():
    form: FilterForm = FilterForm()
    key = 'filtered'
    session.pop(key, None)
    if request.args:
        filters: dict = dict()
        for argument in request.args:
            value = request.args.get(argument)
            if argument in ('year_min', 'year_max', 'age_min', 'age_max') and value:
                filters.setdefault(argument, int(value))
            if value != '__None' and value != '':
                filters.setdefault(argument, request.args.getlist(argument))
        stmt = select(Individ).join(Individ.site).join(Individ.preservation).join(ArchaeologicalSite.researchers).join(Individ.sex).join(ArchaeologicalSite.region)
        print(filters)
        if a := filters.get('epoch'):
            stmt = stmt.join(Individ.epoch).where(getattr(Epoch, 'id').in_(a))
        if b := filters.get('researcher'):
            stmt = stmt.where(getattr(Researcher, 'id').in_(b))
        if c := filters.get('federal_district'):
            stmt = stmt.join(Region.federal_district).where(getattr(FederalDistrict, 'id').in_(c))
        if d := filters.get('year_min'):
            stmt = stmt.where(Individ.year >= d)
        if e := filters.get('year_max'):
            stmt = stmt.where(Individ.year <= e)
        if f := filters.get('sex'):
            stmt = stmt.where(getattr(Sex, 'sex').in_(f))
        if g := filters.get('preservation'):
            stmt = stmt.where(getattr(Preservation, 'id').in_(g))
        if e := filters.get('grave_type'):
            stmt = stmt.join(Individ.grave).where(getattr(Grave, 'grave_type').in_(e))
        if f := filters.get('creator'):
            stmt = stmt.join(Individ.creator).where(getattr(DatabaseUser, 'id').in_(f))
        if i := filters.get('site'):
            stmt = stmt.join(Individ.site).where(getattr(ArchaeologicalSite, 'id').in_(i))
        if s := filters.get('type'):
            stmt = stmt.where(getattr(Individ, 'type').in_(s))
        if z := filters.get('grave'):
            stmt = stmt.join(Individ.grave).where(getattr(Grave, 'grave_number').in_(z))
        if filters.get('age_min') and filters.get('age_max'):
            min = filters.get('age_min')
            max = filters.get('age_max')
            stmt = stmt.where(
                case(
                (Individ.age_max.is_(None), or_(between(Individ.age_min, min, max), Individ.age_min < min)),
                (Individ.age_min.is_(None), Individ.age_max >= min),
                else_ = (or_(between(Individ.age_min, min, max), between(Individ.age_max, min, max)))
                )
                )
        if filters.get('age_min') and not filters.get('age_max'):
            min = filters.get('age_min')
            stmt = stmt.where(
                case(
                (Individ.age_max.is_(None), Individ.age_min >= 0),
                else_ = or_(between(Individ.age_min, min, 200), between(Individ.age_max, min, 200))
                )
                )
        if filters.get('age_max') and not filters.get('age_min'):
            max = filters.get('age_max')
            print('popka')
            stmt = stmt.where(
                case(
                (Individ.age_min.is_(None), Individ.age_max > 0),
                else_ = or_(between(Individ.age_max, 0, max), Individ.age_min <= max)
                )
                )
        global individs
        individs = db.session.scalars(stmt.group_by(Individ.id).order_by(Individ.index)).all()
        session[key] = individs
        return render_template('individ/individ_table.html',
                               title='Таблица индивидов',
                               individs=enumerate(individs, 1),
                               form=form,
                               key=key,
                               action=url_for('individ.search'))
    return redirect(url_for('individ.individ_table'))


@bp.route('/by_site/<site_id>', methods=['GET', 'POST'])
@login_required
def individs_by_site(site_id):
    stmt = select(Individ).join(Individ.site).where(ArchaeologicalSite.id==site_id)
    individs = db.session.scalars(stmt.group_by(Individ.id).order_by(Individ.index)).all()
    key = f'site_{site_id}_individs'
    session.pop(key, None)
    session.setdefault(key, individs)
    return render_template('individ/individ_table.html', title='Таблица индивидов', key=key, individs=enumerate(individs, 1))