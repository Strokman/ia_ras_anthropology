from src.base_habilis.cli import bp
from src.repository import session
from os import path, listdir
from collections import defaultdict
import pandas as pd
import re
import pprint

from src.repository.models import Epoch, FederalDistrict, Region, Preservation, Sex, Individ, ArchaeologicalSite, Grave, User, Researcher, Comment
from csv import DictReader

from sqlalchemy import select

import warnings

warnings.simplefilter("ignore")


@bp.cli.command("fix-graves")
def fix_graves():
    stmt = select(Grave)
    session.execute(stmt).scalars().all()
    session.commit()


@bp.cli.command("drop-regions")
def drop_regions():
    stmt = select(Region)
    res = session.execute(stmt).scalars().all()
    for i in res:
        i.delete()
    session.commit()


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
    
