from src.base_habilis.cli import bp
from src.repository import session
from os import path

from src.repository.models import Epoch, FederalDistrict, Region,  Preservation, Sex
from csv import DictReader


@bp.cli.command("create-tables")
def create_table():
    all_distr = FederalDistrict.get_all()
    if len(all_distr) > 0:
        print('already created')
    else:
        """ДОБАВЛЕНИЕ ЭПОХ"""
        epochs = ["Палеолит",
                "Мезолит",
                "Неолит",
                "Энеолит",
                "Ранний бронзовый век",
                "Средний бронзовый век",
                "Поздний бронзовый век",
                "Ранний железный век",
                "Античное время",
                "Эпоха переселения народов",
                "Раннее средневековье",
                "Развитое средневековье",
                "Позднее средневековье",
                "Новое время"]
        for i in epochs:
            epoch = Epoch(name=i)
            session.add(epoch)
            session.commit()

        """ДОБАВЛЕНИЕ РЕГИОНОВ И ФО"""
        fo = set()
        reg = {}
        with open(f'{path.dirname(__file__)}/regions.csv', 'r') as f:
            a = DictReader(f, delimiter=',')
            for i in a:
                if i['federal_district']:
                    fo.add(i['federal_district'])
                if i['name_with_type']:
                    reg.setdefault(i['name_with_type'], i['federal_district'])

        for dictrict in fo:
            dist = FederalDistrict(name=dictrict)
            session.add(dist)
        session.commit()
        for k, v in reg.items():
            if v:
                region = Region(name=k, federal_districts_id=session.query(FederalDistrict).filter_by(name=v).first().id)
                session.add(region)
        session.commit()


        """ДОБАВЛЕНИЕ ПОЛА"""
        sex = ('не определен', 'мужской', 'женский')
        for i in sex:
            b = Sex(sex=i)
            b.save()


        """ДОБАВЛЕНИЕ СОХРАННОСТИ"""
        preservation_rates = ('плохая', 'удовлетворительная', 'средняя', 'хорошая')
        for i in preservation_rates:
            d = Preservation(i)
            session.add(d)
        session.commit()

        print('Tables created')
