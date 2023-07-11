from flask import redirect, url_for, render_template, flash, jsonify, request
from flask_login import login_required, current_user
from anthropos import db
from .forms import FilterForm
from anthropos.data import bp
from anthropos.models import Grave, Individ, Researcher, ArchaeologicalSite
from datetime import datetime
from sqlalchemy import select

@bp.route('/individ_data', methods=['GET', 'POST'])
@login_required
def individ_data():
    individs = Individ.get_all(db.session)
    # sorted(Individ.get_all(db.session), key=lambda x: x.index)
    # for i in individs:
    #     print(i.site.researcher)
    
    
    form = FilterForm()
    if form.validate_on_submit():
        stmt = select(Individ).join(Individ.site).join(ArchaeologicalSite.researcher).where(Researcher.id==form.researcher.data.id)
        # researcher = form.researcher.data
        # print(a := researcher.sites)
        # for b in a:
        #     print(type(b))
        #     print(b.name)
        #     print(b.individ)
        individs = db.session.scalars(stmt).all()
        return render_template('data_output.html', individs=individs, form=form)
        # pass
    return render_template('data_output.html', individs=individs, form=form)