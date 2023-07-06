from anthropos.index import bp
from anthropos.site import bp as site_bp
from anthropos.models import DatabaseUser
from anthropos import db
from flask import flash, render_template, url_for
# from anthropos.models import Epoch, FederalDistrict, Region, Sex, Preservation
# from csv import DictReader

@bp.route('/')
@bp.route('/index')
def index():
    # """ДОБАВЛЕНИЕ ЭПОХ"""
    # epochs = ["Палеолит",
    #             "Мезолит",
    #             "Неолит",
    #             "Энеолит",
    #             "Ранний бронзовый век",
    #             "Средний бронзовый век",
    #             "Поздний бронзовый век",
    #             "Ранний железный век",
    #             "Античное время",
    #             "Эпоха переселения народов",
    #             "Раннее средневековье",
    #             "Развитое средневековье",
    #             "Позднее средневековье",
    #             "Новое время"]
    # for i in epochs:
    #     epoch = Epoch(name=i)
    #     db.session.add(epoch)
    # db.session.commit()

    # """ДОБАВЛЕНИЕ РЕГИОНОВ И ФО"""
    # fo = set()
    # reg = dict()
    # with open('/Users/antonstrokov/PycharmProjects/ia_ras_anthropology/region.csv', 'r') as f:
    #     a = DictReader(f, delimiter=',')
    #     for i in a:
    #         if i['federal_district']:
    #             fo.add(i['federal_district'])
    #         if i['name_with_type']:
    #             reg.setdefault(i['name_with_type'], i['federal_district'])

    # for dictrict in fo:
    #     dist = FederalDistrict(name=dictrict)
    #     db.session.add(dist)
    # db.session.commit()
    # for k, v in reg.items():
    #     if v:
    #         region = Region(name=k, federal_districts_id=db.session.query(FederalDistrict).filter_by(name=v).first().id)
    #         db.session.add(region)
    # db.session.commit()


    # """ДОБАВЛЕНИЕ ПОЛА"""
    # sex = ('не определен', 'мужской', 'женский')
    # for i in sex:
    #     b = Sex(sex=i)
    #     b.save_to_db(db.session)


    # """ДОБАВЛЕНИЕ СОХРАННОСТИ"""
    # preservation_rates = ('плохая', 'удовлетворительная', 'средняя', 'хорошая')
    # for i in preservation_rates:
    #     d = Preservation(i)
    #     db.session.add(d)
    # db.session.commit()

    flash('Hello', 'success')
    return render_template('index/index.html', title='Index')
