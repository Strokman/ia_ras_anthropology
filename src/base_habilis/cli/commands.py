from src.base_habilis.cli import bp
from src.repository import session
from os import path, listdir
from math import ceil, trunc
import pandas as pd
import re
from flask import current_app


from datetime import datetime
from src.repository.models import Epoch, FederalDistrict, Region,  Preservation, Sex, Individ, ArchaeologicalSite, Grave, User, Researcher, Comment
from csv import DictReader

from sqlalchemy import select

import warnings

warnings.simplefilter("ignore")

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


@bp.cli.command("restore")
def existed():
    kurgan_regex = r'(?i)кург[^\s]*\s*\d{1,}(?![./\-\+])'
    individ_regex = r'(?i)инд[^\s]*\s*\d{1,}(?![./\-\+])'
    kost_regex = r'(?i)кост[^\s]*\s*\d{1,}(?![./\-\+])'
    grave_regex = r'(?i)п[^\s]*\s*\d{1,}(?![./\-\+])'
    pathname = f'{path.dirname(__file__)}/db_old'
    folder = listdir(pathname)
    try:
        folder.remove('.DS_Store')
    except:
        pass
    pathname = f'{path.dirname(__file__)}/db_old'
    to_drop = ['Координаты', 'Шифр', 'Автор раскопок', 'Регион', 'Район', 'Автор']
    corrupted = []
    counter = 0
    user = session.execute(select(User).filter_by(username='strokman')).scalar_one()
    for file in folder:
        with open(f'{pathname}/{file}', 'rb') as f:
            df = pd.read_excel(f, engine="openpyxl")
            df.drop(to_drop, inplace=True, axis=1)
            site_name = df['Памятник'].unique()[0]
            site = session.execute(select(ArchaeologicalSite).filter_by(name=site_name)).scalars().one()
            to_replace = ['Средневековье',
                          'Будет определено позже',
                          'Кремация',
                          'Ингумация',
                          'Мужской',
                          'Женский',
                          'Не определен',
                          'Курганный',
                          'Грунтовый',
                          'Другое',
                          'Ингумация',
                          'Кремация',
                          'Очень плохая',
                          'Плохая', 
                          'Средняя',
                          'Хорошая']
            replace_with = ['Развитое средневековье',
                            '',
                            'кремация',
                            'ингумация',
                            'мужской',
                            'женский',
                            'не определен',
                            'курганный',
                            'грунтовый',
                            'другой',
                            'ингумация',
                            'кремация',
                            1,
                            2,
                            3,
                            4]
            df.replace(to_replace, replace_with, inplace=True)
            for index, row in df.iterrows():
                individ_data = {}
                age = row['Возраст'].replace(',', '.') if isinstance(row['Возраст'], str) else None
                try:
                    int(row['Номер погребения'])
                    grave_data = {
                        'grave_number': int(row['Номер погребения']),
                        'grave_type': row['Тип погребения']
                    }
                except:
                    try:
                        float(row['Номер погребения'])
                        corrupted.append(df.loc[index])
                        continue
                    except:
                        grave_number = row['Номер погребения'].lower()
                        grave_data = {}
                        if 'кург' in grave_number and 'погр' in grave_number and 'инд' in grave_number: 
                            grave_data['grave_type'] = row['Тип погребения']
                            kurgan_num = re.findall(kurgan_regex, grave_number)
                            grave_num = re.findall(grave_regex, grave_number)
                            skeleton_num = re.findall(individ_regex, grave_number)
                            try:
                                grave_data['skeleton'] = skeleton_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                            try:
                                grave_data['grave_number'] = int(grave_num[0].split()[1])
                            except:
                                corrupted.append(df.loc[index])
                                continue
                            try:
                                grave_data['kurgan_number'] = kurgan_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                        elif 'кург' in grave_number and 'погр' in grave_number:
                            grave_num = re.findall(grave_regex, grave_number)
                            grave_data['grave_type'] = row['Тип погребения']
                            kurgan_num = re.findall(kurgan_regex, grave_number)
                            try:
                                grave_data['grave_number'] = int(grave_num[0].split()[1])
                            except:
                                corrupted.append(df.loc[index])
                                continue
                            try:
                                grave_data['kurgan_number'] = kurgan_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                        elif 'кург' in grave_number and 'инд' in grave_number:
                            grave_num = re.findall(grave_regex, grave_number)
                            grave_data['grave_type'] = row['Тип погребения']
                            grave_data['grave_number'] = 0
                            kurgan_num = re.findall(kurgan_regex, grave_number)
                            skeleton_num = re.findall(individ_regex, grave_number)
                            try:
                                grave_data['kurgan_number'] = kurgan_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                            try:
                                grave_data['skeleton'] = skeleton_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                        elif 'кург' in grave_number and 'п.' in grave_number:
                            grave_data['grave_type'] = row['Тип погребения']
                            kurgan_num = re.findall(kurgan_regex, grave_number)
                            grave_num = re.findall(grave_regex, grave_number)
                            try:
                                grave_data['grave_number'] = int(grave_num[0].split()[1])
                            except:
                                corrupted.append(df.loc[index])
                                continue
                            try:
                                grave_data['kurgan_number'] = kurgan_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                        elif 'кург' in grave_number and 'кост' in grave_number:
                            grave_num = re.findall(grave_regex, grave_number)
                            grave_data['grave_type'] = row['Тип погребения']
                            grave_data['grave_number'] = 0
                            kurgan_num = re.findall(kurgan_regex, grave_number)
                            skeleton_num = re.findall(kost_regex, grave_number)
                            try:
                                grave_data['kurgan_number'] = kurgan_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                            try:
                                grave_data['skeleton'] = skeleton_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                        elif 'кург' in grave_number and 'кост' not in grave_number and 'инд' not in grave_number and 'погр' not in grave_number and 'п.' not in grave_number:
                            grave_data['grave_type'] = row['Тип погребения']
                            grave_data['grave_number'] = 0
                            kurgan_num = re.findall(kurgan_regex, grave_number)
                            try:
                                grave_data['kurgan_number'] = kurgan_num[0].split()[1]
                            except:
                                corrupted.append(df.loc[index])
                                continue
                        else:
                            corrupted.append(df.loc[index])
                            continue   
                if isinstance(age, str):
                    if '+' in age:
                        individ_data['age_min'] = int(age.replace('+', ''))
                    if '-' in age and age[-1] == '-':
                        individ_data['age_min'] = int(age.replace('-', ''))
                    if '-' in age and age[-1] != '-':
                        try:
                            age_min, age_max = age.split('-')
                            individ_data['age_min'] = trunc(float(age_min))
                            individ_data['age_max'] = ceil(float(age_max))
                        except:
                            corrupted.append(df.loc(index))
                            continue
                counter += 1
                individ_data['year'] = row['Год раскопок']
                individ_data['type'] = row['Тип индивида'].lower()
                individ_data['created_by'] = user.id
                individ_data['edited_by'] = user.id
                sex_data = {'sex': row['Пол']}
                preservation_data = {'id': row['Сохранность']}
                if row['Период']:
                    epoch_data = {'name': row['Период']}
                sex = session.execute(select(Sex).filter_by(**sex_data)).scalars().one()
                preservation = session.execute(select(Preservation).filter_by(**preservation_data)).scalars().one()
                try:
                    epoch = session.execute(select(Epoch).filter_by(**epoch_data)).scalars().one()
                except:
                    pass
                grave = Grave(**grave_data)
                individ = Individ(**individ_data)
                comment = Comment(text=f"Исходные данные, погребение: {row['Номер погребения']}, возраст: {row['Возраст']}")
                session.add_all([grave, individ, comment])
                individ.grave = grave
                individ.comment = comment
                preservation.individ.append(individ)
                site.individs.append(individ)
                individ.create_index()
                sex.individs.append(individ)
                if epoch:
                    epoch.individ.append(individ)
            session.commit()
    path_to_file: str = path.join(current_app.root_path,
                                  current_app.config['UPLOAD_FOLDER'],
                                  "corrupted.xlsx")
    corrupted_records = pd.DataFrame(corrupted)
    corrupted_records.to_excel(path_to_file, sheet_name='corrupted')


@bp.cli.command("sites")
def sites():
    sites = {'Колбино I', 'Дуровка', 'Терновое 1', 'Никольское III', 'Горки I', 'Воезеро 1', 'Минино II', 'Девица 5', 'Шуйгино', 'Нефедьево', 'Льговский курган'}
    researcher = session.execute(select(Researcher).filter_by(id=16)).scalar_one()
    user = session.execute(select(User).filter_by(username='strokman')).scalar_one()
    site_dict = {
        'long': 1,
        'lat': 2,
        'created_by': user.id,
        'edited_by': user.id,
        'region_id': 14
    }
    for i in sites:
        site_dict['name'] = i
        site = ArchaeologicalSite(**site_dict)
        session.add(site)
        researcher.sites.append(site)
    session.commit()


@bp.cli.command("delete-individs")
def delete():
    stmt = select(Individ).where(Individ.created_at > datetime(2023, 10, 1))
    individs = session.execute(stmt).scalars().all()
    for individ in individs:
        individ.delete()
