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

