from flask import redirect, url_for, render_template, flash, jsonify, request
from flask_login import login_required, current_user
from anthropos import db
from .forms import FilterForm
from anthropos.data import bp
from anthropos.models import Sex, Individ, Researcher, ArchaeologicalSite, Epoch, FederalDistrict, Region, Preservation
from datetime import datetime
from sqlalchemy import select


@bp.route('/individ_data', methods=['GET', 'POST'])
@login_required
def individ_data():
    individs = Individ.get_all(db.session)
    form = FilterForm()
    return render_template('data_output.html', individs=individs, form=form)


@bp.route('/individ_filter', methods=['GET', 'POST'])
@login_required
def search():
    form = FilterForm()
    if request.args:
        b = request.args
        args_dict = dict()
        for i in b:
            temp = b.get(i)
            if i in ('year_min', 'year_max'):
                args_dict.setdefault(i, temp)
            if temp != '__None':
                args_dict.setdefault(i, b.getlist(i))
        stmt = select(Individ).join(Individ.site).join(Individ.preservation).join(ArchaeologicalSite.researcher).join(Individ.sex).join(Individ.editor).join(ArchaeologicalSite.epochs).join(ArchaeologicalSite.regions).join(Region.federal_district)
        if a := args_dict.get('epoch'):
            stmt = stmt.where(getattr(Epoch, 'id').in_(args_dict.get('epoch')))
        if b := args_dict.get('researcher'):
            stmt = stmt.where(getattr(Researcher, 'id').in_(args_dict.get('researcher')))
        if c := args_dict.get('federal_district'):
            stmt = stmt.where(getattr(FederalDistrict, 'id').in_(args_dict.get('federal_district')))
        if d := args_dict.get('year_min'):
            stmt = stmt.where(Individ.year >= d)
        if e := args_dict.get('year_max'):
            stmt = stmt.where(Individ.year <= e)
        if f := args_dict.get('sex'):
            stmt = stmt.where(getattr(Sex, 'sex').in_(f))
        if g := args_dict.get('preservation'):
            stmt = stmt.where(getattr(Preservation, 'id').in_(g))
        print(stmt)
        individs=db.session.scalars(stmt.group_by(Individ.id)).all()
        return render_template('data_output.html', individs=individs, form=form)
    return redirect(url_for('data.individ_data'))