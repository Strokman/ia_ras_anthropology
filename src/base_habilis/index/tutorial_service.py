import os
from flask import url_for


class TutorialText:

    SCREEN_1 = """
    Для регистрации или входа в систему - нажмите кнопку Вход.
    """

    SCREEN_2 = """
    Далее, при регистрации - нажмите соотв. кнопку.
    """

    SCREEN_3 = """
    1. Зарегистрируйтесь, заполнив нужные поля.
    2. Логин - не адрес почты!
    3. Место работы и почта - не обязательны.
    """

    SCREEN_4 = """
    1. После корректного заполнения всех полей - Вам будет выслана ссылка на адрес эл. почты.
    2. Пройдите по ней - после этого Вы сможете войти в систему.
    3. Если Вы забыли или хотитет поменять пароль - на странице логина есть такая кнопка.
    """


    SCREEN_5 = """
    1. Процедура внесения следующая - сначала вносим исследователя, затем памятник, затем индивидов.
    2. При внесении исследователя - обязательны все поля, кроме отчества.
    """

    SCREEN_6 = """
    1. При внесении памятников - все поля, кроме эпох, обязательны.
    2. Для названия памятника - выбирайте короткое, емкое название:
    не пишите, если в отчете указано что-то вроде "Культурный слой города такого-то 18-20 вв".
    Достаточно основного названия памятника.
    3. Поля широта и долгота принимают только целые числа и числа с плавающей запятой (дробные).
    4. Эпох можно выбрать несколько, одну или не выбирать (см. выше).
    5. Исследователи выбираются из тех, которые уже внесены в базу.
    6. Федеральные округа и регионы (области) - из сохраненных мною заранее в базу.
    """

    SCREEN_7 = """
    Внесение индивидов подробнее
    1. Обязательные поля:
    - памятник (выбирается из уже внесенных в базу)
    - год исследования (только целые числа!)
    - обряд (выбирается из предустановленных)
    - пол (выбирается из предустановленных)
    - тип памятника (также из предустановленных)
    - номер погребения (только число! он нужен для формирования шифра, поэтому не может быть не заполнен)
    2. Все остальные поля - не обязательны
    3. Эпоха - выбирается из предустановленных. Можно выбрать только одну.
    4. Сохранность: градация слева направо - плохая, удовлетворительная, средняя, хорошая
    """

    SCREEN_8 = """
    1. Возраст - только целые числа! Если нерожденный или что-то вроде того - ставить 0 - 0.
    Если младенец - можно поставить макс. возраст 1.
    2. Файл только один и формата пдф или jpg. Не более 100 мб
    3. Примчание - любой текст. Есть базовый поиск по примечаниям.
    """

    SCREEN_9 = """
    1. Как уже было сказано - обязательно указать тип памятника и номер погребения.
    2. Если вдруг нет номера погребения - в номер погр. ставить 0.
    3. Номер погребения - только целые числа!
    4. В остальные поля можно записать все, что угодно, но вы должны понимать, что это усложнит поиск и фильтрацию.
    """
    
    def __init__(self, current_app) -> None:
        self.current_app = current_app
        
    def create_tutorial(self):
        tutorial_files = os.listdir(self.current_app.root_path + self.current_app.static_url_path + '/tutorial')
        urls = []
        for file in tutorial_files:
            urls.append(url_for('static', filename=f'tutorial/{file}'))
        urls.sort()
        tutorial = dict(zip([getattr(self, k) for k in dir(self) if not k.startswith('_')], urls))
        return tutorial
