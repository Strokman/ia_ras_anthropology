from anthropos import db, app
from csv import DictReader
from anthropos.models import Comment, Epoch, File, Grave, Individ, Preservation, Researcher, Sex,\
    sites_epochs, ArchaeologicalSite, DatabaseUser, FederalDistrict, Region
#
#
def create_tables():
    with app.app_context():
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
            db.session.add(epoch)
        db.session.commit()

        """ДОБАВЛЕНИЕ РЕГИОНОВ И ФО"""
        fo = set()
        reg = dict()
        with open('/Users/antonstrokov/PycharmProjects/ia_ras_anthropology/region.csv', 'r') as f:
            a = DictReader(f, delimiter=',')
            for i in a:
                if i['federal_district']:
                    fo.add(i['federal_district'])
                if i['name_with_type']:
                    reg.setdefault(i['name_with_type'], i['federal_district'])

        for dictrict in fo:
            dist = FederalDistrict(name=dictrict)
            db.session.add(dist)
        db.session.commit()
        for k, v in reg.items():
            if v:
                region = Region(name=k, federal_districts_id=db.session.query(FederalDistrict).filter_by(name=v).first().id)
                print(region.federal_district)
                db.session.add(region)
        db.session.commit()


        """ДОБАВЛЕНИЕ ПОЛА"""
        sex = ('male', 'female')
        for i in sex:
            b = Sex(sex=i)
            db.session.add(b)
        db.session.commit()


        """ДОБАВЛЕНИЕ СОХРАННОСТИ"""
        preservation_rates = ('плохая', 'удовлетворительная', 'средняя', 'хорошая')
        for i in preservation_rates:
            d = Preservation(i)
            db.session.add(d)
        db.session.commit()

if __name__ == '__main__':
    create_tables()
