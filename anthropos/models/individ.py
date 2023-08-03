from anthropos import db
from .base_model import BaseModel
from flask_moment import moment


class Individ(db.Model, BaseModel):
    __tablename__ = 'individs'

    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(128))
    year = db.Column(db.Integer)
    age_min = db.Column(db.Integer)
    age_max = db.Column(db.Integer)
    type = db.Column(db.String(16))
    created_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime)
    sex_type = db.Column(db.String, db.ForeignKey('sex.sex'))
    site_id = db.Column(db.Integer, db.ForeignKey('archaeological_sites.id'))
    epoch_id = db.Column(db.Integer, db.ForeignKey('epochs.id'))
    created_by = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    edited_by = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    preservation_id = db.Column(db.Integer, db.ForeignKey('preservation.id'))

    site = db.relationship('ArchaeologicalSite', back_populates='individ')
    comment = db.relationship('Comment', uselist=False, back_populates='individ', cascade='all, delete-orphan')
    epoch = db.relationship('Epoch', uselist=False, back_populates='individ')
    creator = db.relationship("DatabaseUser", foreign_keys='Individ.created_by', back_populates='individs_created')
    editor = db.relationship("DatabaseUser", foreign_keys='Individ.edited_by', back_populates='individs_edited')
    sex = db.relationship('Sex', back_populates='individ')
    preservation = db.relationship('Preservation', back_populates='individ')
    file = db.relationship('File', back_populates='individ', uselist=False, cascade='all, delete-orphan')
    grave = db.relationship('Grave', uselist=False, back_populates='individ', cascade='all, delete-orphan')

    def create_index(self):
        if self.grave.grave_type == 'курганный' and self.grave.kurgan_number:
            self.index = f'{self.site.name}-{self.year}-к{self.grave.kurgan_number}-п{self.grave.grave_number}'.replace(' ', '-').replace('/', '-').replace('\\', '-')
        else:
            self.index = f'{self.site.name}-{self.year}-п{self.grave.grave_number}'.replace(' ', '-').replace('/', '-').replace('\\', '-')

    def __repr__(self):
        return f'{self.index}'

    def age(self):
        if self.age_min and self.age_max:
            return f'{self.age_min}-{self.age_max}'
        if self.age_min:
            return f'{self.age_min}+'
        if self.age_max and not self.age_min:
            return f'до {self.age_max}'
        return ''
    
    def dict_russian(self):
        return {
            'ID': self.id,
            'Индекс': self.index,
            'Год раскопок': self.year,
            'Памятник': self.site,
            'Погребение': self.grave.__str__(),
            'Федеральный округ': self.site.region.federal_district,
            'Область': self.site.region,
            'Долгота': self.site.long,
            'Широта': self.site.lat,
            'Автор раскопок': ''.join((researcher.__repr__() for researcher in self.site.researchers)),
            'Эпоха': self.epoch if self.epoch else '',
            'Тип погребения': self.grave.grave_type,
            'Возраст': self.age(),
            'Пол': self.sex.sex,
            'Сохранность': self.preservation.description,
            'Примечание': self.comment.text,
            'Кем создано': self.creator,
            'Когда создано': moment(self.created_at).format('L'),
            'Кем изменено': self.editor,
            'Когда изменено': moment(self.edited_at).format('L')
        }
