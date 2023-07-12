from flask import redirect, url_for, render_template, flash, jsonify, request
from flask_login import login_required, current_user
from anthropos import db
from .forms import FilterForm
from anthropos.data import bp
from anthropos.models import Grave, Individ, Researcher, ArchaeologicalSite, Epoch, FederalDistrict, Region
from datetime import datetime
from sqlalchemy import select


@bp.route('/individ_data', methods=['GET', 'POST'])
@login_required
def individ_data():
    individs = Individ.get_all(db.session)
    form = FilterForm()
    if request.args:
        b = request.args
        argslist = dict()
        for i in b:
            print(i)
            print(b.get(i), '-', len(b.get(i)))
            argslist.setdefault(i, b.getlist(i))
        print(argslist)
        print(argslist.get('lulka'))
        last_stmt = select(Individ).filter_by().\
                    join(ArchaeologicalSite).where(Individ.year >= request.args.get('year_min'), Individ.year <= request.args.get('year_max')).\
                    join(Epoch, ArchaeologicalSite.epochs).\
                    where(Epoch.id.in_(b.getlist('epoch'))).\
                    join(Researcher).filter_by(id=request.args.get('researcher')).\
                    join(Region).\
                    join(FederalDistrict).filter_by(id=request.args.get('federal_district'))
        # if form.validate_on_submit():
        # stmt = select(Individ).join(Individ.site).join(ArchaeologicalSite.researcher).where(Researcher.id==form.researcher.data.id)
            # researcher = form.researcher.data
            # print(a := researcher.sites)
            # for b in a:
            #     print(type(b))
            #     print(b.name)
            #     print(b.individ)
        individos = db.session.scalars(last_stmt)
        print(individos)
        return render_template('data_output.html', individs=individs, form=form)

    return render_template('data_output.html', individs=individs, form=form)