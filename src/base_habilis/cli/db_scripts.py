from src.base_habilis.cli import bp
from src.repository import session
from os import path, listdir
from collections import defaultdict
import pandas as pd
import re
import pprint
from src.services import geocode
from src.repository.models import Epoch, Country, Region, Preservation, Sex, Individ, ArchaeologicalSite, Grave, User, Researcher
from csv import DictReader
from decimal import Decimal
from sqlalchemy import select

import warnings

warnings.simplefilter("ignore")


@bp.cli.command("fix-graves")
def fix_graves():
    stmt = select(Grave)
    res = session.execute(stmt).scalars().all()
    for i in res:
        if not i.site:
            i.site = i.individ.site
            print(i.site)
    session.commit()


@bp.cli.command("drop-regions")
def drop_regions():
    stmt = select(Country)
    res = session.execute(stmt).scalars().all()
    for i in res:
        i.delete()
    session.commit()


@bp.cli.command("fix-regions")
def fix_regions():
    stmt = select(ArchaeologicalSite)
    res = session.execute(stmt).scalars().all()
    for site in res:
        long = site.long
        lat = site.lat
        region_data = geocode.get_location_data(geocode.create_geocode_url(lat, long))
        region = Region.get_one_by_attr('name', session, region_data['region'])
        country = Country.get_one_by_attr('name', session, region_data['country'])
        if not country:
            country = Country.create(name=region_data['country'])
        if not region:
            region = Region.create(name=region_data['region'])
            country.region.append(region)
        region.sites.append(site)
    session.commit()


# @bp.cli.command("migrate-comments")
# def migrate_comments():
#     stmt = select(Individ)
#     res = session.execute(stmt).scalars().all()
#     for individ in res:
#         try:
#             individ.comment_temp = individ.comment.text
#         except:
#             pass
#     session.commit()

# @bp.cli.command("fix-skeletons")
# def fix_skeletons():
#     stmt = select(Grave).group_by(Grave.id, Grave.grave_number)
#     res = session.execute(stmt).scalars().all()
#     graves_dict = defaultdict(list)
#     for i in sorted(res, key=lambda x: x.grave_number):
#         graves_dict[i.site].append(i)
#     for k, v in graves_dict.items():
#         b = defaultdict(list)
#         for j in v:
#             b[j.grave_number].append(j)
#         graves_dict[k] = b
#     for k, v in graves_dict.items():
#         for i, j in v.items():
#             for i in range(len(j)):
#                 if j[i].skeleton is None or j[i].skeleton == 0:
#                     j[i].skeleton = i + 1
#                 pprint.pprint(j)
    # session.commit()
    
