from os import path, remove

import pandas as pd
from flask import Flask

from src.repository.models.individ import Individ


def export_xls(individs: list[Individ],
               current_app: Flask,
               export_name: str = 'default') -> str:

    export_data: dict = {}

    export_data.setdefault('Индекс', [individ.index for individ in individs])
    export_data.setdefault('Памятник', [individ.site for individ in individs])
    export_data.setdefault('Погребение',
                           [individ.grave for individ in individs])
    export_data.setdefault('Эпоха', [individ.epoch for individ in individs])
    export_data.setdefault('Исследователь',
                           [', '.join(researcher.__repr__()
                            for researcher in individ.site.researchers)
                            for individ in individs])
    export_data.setdefault('Федеральный округ',
                           [individ.site.region.federal_district
                            for individ in individs])
    export_data.setdefault('Регион',
                           [individ.site.region for individ in individs])
    export_data.setdefault('Долгота',
                           [individ.site.long for individ in individs])
    export_data.setdefault('Широта',
                           [individ.site.lat for individ in individs])
    export_data.setdefault('Год', [individ.year for individ in individs])
    export_data.setdefault('Возраст', [individ.age() for individ in individs])
    export_data.setdefault('Обряд', [individ.type for individ in individs])
    export_data.setdefault('Пол', [individ.sex for individ in individs])
    export_data.setdefault('Сохранность',
                           [individ.preservation for individ in individs])
    export_data.setdefault('Примечание',
                           [individ.comment for individ in individs])
    export_data.setdefault('Кем создано',
                           [individ.creator for individ in individs])
    export_data.setdefault('Создано',
                           [individ.created_at for individ in individs])
    export_data.setdefault('Кем изменено',
                           [individ.editor for individ in individs])
    export_data.setdefault('Изменено',
                           [individ.edited_at for individ in individs])

    path_to_file: str = path.join(current_app.root_path,
                                  current_app.config['UPLOAD_FOLDER'],
                                  f"{export_name}.xlsx")
    if path.isfile(path_to_file):
        remove(path_to_file)
    df: pd.DataFrame = pd.DataFrame(export_data,
                                    [pd.Index(range(1, len(individs) + 1))])
    df['Создано'] = df['Создано'].dt.tz_localize('UTC').\
        dt.tz_convert('Europe/Moscow').dt.tz_localize(None)
    df['Изменено'] = df['Изменено'].dt.tz_localize('UTC').\
        dt.tz_convert('Europe/Moscow').dt.tz_localize(None)
    df.to_excel(path_to_file, sheet_name=export_name)
    return path_to_file
