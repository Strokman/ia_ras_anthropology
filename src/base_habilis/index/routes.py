# import os

from flask import render_template, current_app

from src.base_habilis.index import bp
from src.base_habilis.index.tutorial_service import TutorialText

from src.repository.models import Region, Individ
from src.repository import session
from src.core.models import RegionCore
from src.core.models import IndividCore
from sqlalchemy import select

@bp.route('/')
@bp.route('/index')
def index() -> str:
    instance = TutorialText(current_app)
    tutorial = instance.create_tutorial()
    res = session.execute(select(Region).limit(1)).scalar()
    ind_1 = session.execute(select(Individ).limit(1)).scalar()
    model = IndividCore.model_validate(ind_1)
    print(model.site.researchers[0])
    print(model)
    # distr = res.federal_district
    # mdl = FedDistrClass.model_validate(distr)

    return render_template('index/index.html', title='Домашняя страница', tutorial=tutorial)
