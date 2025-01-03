import datetime

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    session as sess,
    url_for)
from flask_login import current_user, login_required
from sqlalchemy import between, case, or_, select
from sqlalchemy.sql.expression import collate

from src.base_habilis.extensions import csrf
from src.base_habilis.individ.forms import IndividForm, FilterForm
from src.base_habilis.individ import bp
from src.repository.models import (
    Sex,
    Individ,
    Researcher,
    ArchaeologicalSite,
    Epoch,
    Country,
    Region,
    Preservation,
    Grave,
    User)
from src.repository import session, paginate
from src.core.models import IndividCore
from src.core.services.sort import sort_func

from src.services.files.file_service import upload_file_to_s3, s3_client, FileDTO, delete_file_from_s3

@bp.route('/submit_individ', methods=['GET', 'POST'])
@login_required
def submit_individ():
    form = IndividForm()
    if form.validate_on_submit():
        # If form submitted correctly - create instance of Individ class
        individ = Individ(
            year=form.data.get('year', None),
            age_min=form.data.get('age_min', None),
            age_max=form.data.get('age_max', None),
            site_id=form.data.get('site', None).id,
            type=form.data.get('type', None),
            created_at=datetime.datetime.now(datetime.UTC),
            created_by=current_user.id,
            edited_at=datetime.datetime.now(datetime.UTC),
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
        individ.preservation = form.data.get('preservation', None)
        # add both to the session, so that everything
        # will work correct with ID's etc.
        session.add_all((individ, grave))

        # add requiered relations
        individ.grave = grave
        sex = form.sex.data
        sex.individs.append(individ)
        site = form.site.data
        site.graves.append(grave)
        site.individs.append(individ)

        # create index of individ - because it requieres grave it is only here, \
        # after grave is initialized and relation to the individ is added
        individ.create_index()

        # check if file, comment and epoch were submitted, than instanciate everything,\
        #  add to session to create relations
        if form.comment.data:
            individ.comment = form.comment.data

        if epoch := form.epoch.data:
            epoch.individ.append(individ)

        if uploaded_file := form.file.data:
            file_dto = FileDTO.create(uploaded_file)
            upload_file_to_s3(s3_client, file_dto)
            session.add(file_dto.file)
            individ.file = file_dto.file

        # commit all changes to the DB
        session.commit()
        current_app.logger.info(f'Individ created: {individ} by {current_user}')
        flash(f'Индивид {individ} успешно добавлен', 'success')
        return redirect(url_for('individ.submit_individ'))
    return render_template('individ/submit_individ.html', form=form)


@bp.route('/delete_individ/<individ_id>', methods=['POST'])
@csrf.exempt
@login_required
def delete_individ(individ_id):
    individ: Individ | None = Individ.get_by_id(individ_id)
    if individ.file is not None:
        delete_file_from_s3(s3_client, individ.file)
    individ.delete()
    flash('Запись удалена', 'success')
    return redirect(request.referrer)


@bp.route('/edit_individ/<int:individ_id>', methods=['GET', 'POST'])
@login_required
def edit_individ(individ_id):
    individ = Individ.get_by_id(individ_id)
    form = IndividForm()
    if request.method == 'POST' and form.validate_on_submit():
        individ.grave.grave_type = form.data.get('grave_type', None)
        individ.grave.kurgan_number = form.data.get('kurgan_number', None)
        individ.grave.grave_number = form.data.get('grave_number', None)
        individ.grave.catacomb = form.data.get('catacomb', None)
        individ.grave.chamber = form.data.get('chamber', None)
        individ.grave.trench = form.data.get('trench', None)
        individ.grave.area = form.data.get('area', None)
        individ.grave.object = form.data.get('object', None)
        individ.grave.layer = form.data.get('layer', None)
        individ.grave.square = form.data.get('square', None)
        individ.grave.sector = form.data.get('sector', None)
        individ.grave.niveau_point = form.data.get('niveau_point', None)
        individ.grave.tachymeter_point = form.data.get('tachymeter_point', None)
        individ.grave.skeleton = form.data.get('skeleton', None)
        individ.year = form.data.get('year', None)
        individ.age_min = form.data.get('age_min', None)
        individ.age_max = form.data.get('age_max', None)
        individ.preservation = form.data.get('preservation', None)     # ПРОВЕРИТЬ
        individ.type = form.data.get('type', None)
        individ.edited_at = datetime.datetime.now(datetime.UTC),
        individ.edited_by = current_user.id

        sex = form.sex.data
        sex.individs.append(individ)

        if input_comment := form.comment.data:
            individ.comment = input_comment
        elif individ.comment:
            individ.comment = None
        if individ.site != (site := form.site.data):
            site.individ.append(individ)
        individ.create_index()
        if uploaded_file := form.file.data:
            file_dto = FileDTO.create(uploaded_file)
            if individ.file is not None:
                delete_file_from_s3(s3_client, individ.file)
                upload_file_to_s3(s3_client, file_dto)              
            else:
                upload_file_to_s3(s3_client, file_dto)
                session.add(file_dto.file)
            individ.file = file_dto.file
        if epoch := form.epoch.data:
            epoch.individ.append(individ)
        session.commit()
        flash(f'Индивид {individ} успешно отредактирован', 'success')
        return redirect(sess['prev'])
    elif request.method == 'GET':
        sess['prev'] = request.referrer
        form.submit.label.text = 'Редактировать'
        form.site.data = individ.site
        form.sex.data = individ.sex
        form.type.data = individ.type
        form.age_min.data = individ.age_min
        form.age_max.data = individ.age_max
        form.year.data = individ.year
        form.preservation.data = individ.preservation
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
            form.comment.data = individ.comment
    return render_template('individ/submit_individ.html', form=form)


@bp.route('/individ_table/', methods=['GET'])
@bp.route('/individ_table/<string:sort>/', methods=['GET'])
@login_required
def individ_table(sort='index'):
    form: FilterForm = FilterForm()
    stmt = sort_func(sort)
    per_page = 50
    individs = paginate(stmt, per_page=per_page)
    page = int(request.args.get('page', 1))
    key = 'all'
    to_save = [IndividCore.model_validate(individ) for individ in Individ.get_all('index')]
    sess.pop(key, None)
    sess.setdefault(key, to_save)
    return render_template('individ/individ_table.html',
                           title='Таблица индивидов',
                           page=page,
                           per_page=per_page,
                           individs=individs,
                           form=form,
                           key=key,
                           sort=sort,
                           action=url_for('individ.individ_table'))


@bp.route('/individ_filter', methods=['GET'])
@login_required
def search(sort=None):
    form: FilterForm = FilterForm()
    key = 'filtered'
    sess.pop(key, None)
    if request.args:
        filters: dict = dict()
        for argument in request.args:
            value = request.args.get(argument)
            if argument in ('year_min', 'year_max', 'age_min', 'age_max', 'index', 'comment') and value:
                filters.setdefault(argument, value)
            if value != '__None' and value != '':
                filters.setdefault(argument, request.args.getlist(argument))
        stmt = select(Individ).join(Individ.site).join(Individ.preservation).join(ArchaeologicalSite.researchers).join(Individ.sex).join(ArchaeologicalSite.region)
        if index_search_filter := filters.get('index'):
            stmt = stmt.where(Individ.index.ilike(f'%{index_search_filter}%'))
        if epoch_filter := filters.get('epoch'):
            stmt = stmt.join(Individ.epoch).where(getattr(Epoch, 'id').in_(epoch_filter))
        if researcher_filter := filters.get('researcher'):
            stmt = stmt.where(getattr(Researcher, 'id').in_(researcher_filter))
        if country_filter := filters.get('country'):
            stmt = stmt.join(Region.country).where(getattr(Country, 'id').in_(country_filter))
        if year_min_filter := filters.get('year_min'):
            stmt = stmt.where(Individ.year >= year_min_filter)
        if year_max_filter := filters.get('year_max'):
            stmt = stmt.where(Individ.year <= year_max_filter)
        if sex_filter := filters.get('sex'):
            stmt = stmt.where(getattr(Sex, 'sex').in_(sex_filter))
        if preservation_filter := filters.get('preservation'):
            stmt = stmt.where(getattr(Preservation, 'id').in_(preservation_filter))
        if grave_type_filter := filters.get('grave_type'):
            stmt = stmt.join(Individ.grave).where(getattr(Grave, 'grave_type').in_(grave_type_filter))
        if creator_filter := filters.get('creator'):
            stmt = stmt.join(Individ.creator).where(getattr(User, 'id').in_(creator_filter))
        if arch_site_filter := filters.get('site'):
            stmt = stmt.join(Individ.site).where(getattr(ArchaeologicalSite, 'id').in_(arch_site_filter))
        if type_filter := filters.get('type'):
            stmt = stmt.where(getattr(Individ, 'type').in_(type_filter))
        if grave_number_filter := filters.get('grave'):
            stmt = stmt.join(Individ.grave).where(getattr(Grave, 'grave_number').in_(grave_number_filter))
        if comment_filter := filters.get('comment'):
            stmt = stmt.join(Individ.comment).where(Individ.comment.ilike(f'%{comment_filter}%'))
        if filters.get('age_min') and filters.get('age_max'):
            age_min = filters.get('age_min')
            age_max = filters.get('age_max')
            stmt = stmt.where(
                case(
                    (Individ.age_max.is_(None), or_(between(Individ.age_min, age_min, age_max), Individ.age_min < age_min)),
                    (Individ.age_min.is_(None), Individ.age_max >= age_min),
                    else_=(or_(between(Individ.age_min, age_min, age_max), between(Individ.age_max, age_min, age_max)))
                )
                )
        if filters.get('age_min') and not filters.get('age_max'):
            age_min = filters.get('age_min')
            stmt = stmt.where(
                case(
                    (Individ.age_max.is_(None), Individ.age_min >= 0),
                    else_=or_(between(Individ.age_min, age_min, 200), between(Individ.age_max, age_min, 200))
                    )
                )
        if filters.get('age_max') and not filters.get('age_min'):
            age_max = filters.get('age_max')
            stmt = stmt.where(
                case(
                    (Individ.age_min.is_(None), Individ.age_max > 0),
                    else_=or_(between(Individ.age_max, 0, age_max), Individ.age_min <= age_max)
                    )
                )
        stmt = stmt.group_by(Individ.id).order_by(collate(Individ.index, "numeric"))
        individs = session.scalars(stmt).all()
        to_save = [IndividCore.model_validate(individ) for individ in individs]
        sess[key] = to_save
        return render_template('individ/individ_filter.html',
                               title='Таблица индивидов',
                               individs=individs,
                               form=form,
                               key=key,
                               action=url_for('individ.search'))
    return redirect(url_for('individ.individ_table'))


@bp.route('/by-site/<int:site_id>', methods=['GET', 'POST'])
@bp.route('/by-site/<int:site_id>/<string:sort>', methods=['GET'])
@login_required
def individs_by_site(site_id, sort=None):
    filter = {'site_id': site_id}
    stmt = sort_func(sort, filter)
    individs = session.scalars(stmt).all()
    key = f'site_{site_id}_individs'
    to_save = [IndividCore.model_validate(individ) for individ in individs]
    sess.pop(key, None)
    sess.setdefault(key, to_save)
    print(site_id)
    return render_template('map/individ_by_site.html', title='Таблица индивидов', site_id=site_id, key=key, individs=individs)
