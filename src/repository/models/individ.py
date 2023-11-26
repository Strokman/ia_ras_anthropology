from src.repository import Column, relationship, ForeignKey, Integer, DateTime, String, Model
from src.repository import BaseModel
from flask_moment import moment
from datetime import datetime


class Individ(BaseModel, Model):
    __tablename__ = 'individs'

    id = Column(Integer, primary_key=True)
    index = Column(String(128))
    year = Column(Integer)
    age_min = Column(Integer)
    age_max = Column(Integer)
    type = Column(String(16))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    edited_at = Column(DateTime, default=datetime.utcnow)
    sex_type = Column(String, ForeignKey('sex.sex'))
    site_id = Column(Integer, ForeignKey('archaeological_sites.id'))
    epoch_id = Column(Integer, ForeignKey('epochs.id'))
    created_by = Column(Integer, ForeignKey("users.id"))
    edited_by = Column(Integer, ForeignKey("users.id"))
    preservation_id = Column(Integer, ForeignKey('preservation.id'))

    site = relationship('ArchaeologicalSite', back_populates='individs')
    comment = relationship('Comment', uselist=False, back_populates='individ', cascade='all, delete-orphan')
    epoch = relationship('Epoch', uselist=False, back_populates='individ')
    creator = relationship("User", uselist=False, foreign_keys='Individ.created_by', back_populates='individs_created')
    editor = relationship("User", uselist=False, foreign_keys='Individ.edited_by', back_populates='individs_edited')
    sex = relationship('Sex', back_populates='individs')
    preservation = relationship('Preservation', back_populates='individ')
    file = relationship('File', back_populates='individ', uselist=False, cascade='all, delete-orphan')
    grave = relationship('Grave', uselist=False, back_populates='individ', cascade='all, delete-orphan')

    def create_index(self):
        if self.grave.grave_type == 'курганный' and self.grave.kurgan_number:
            self.index = f'{self.site.name}-{self.year}-к{self.grave.kurgan_number}-п{self.grave.grave_number}'.replace(' ', '-').replace('/', '-').replace('\\', '-')
        else:
            self.index = f'{self.site.name}-{self.year}-п{self.grave.grave_number}'.replace(' ', '-').replace('/', '-').replace('\\', '-')

    def __repr__(self):
        return f'{self.index}'

    @property
    def age(self):
        if self.age_min and self.age_max:
            return f'{self.age_min}-{self.age_max}'
        if self.age_min:
            return f'{self.age_min}+'
        if self.age_max and not self.age_min:
            return f'до {self.age_max}'
        return None
    
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
            'Возраст': self.age,
            'Пол': self.sex.sex,
            'Сохранность': self.preservation.description,
            'Примечание': self.comment.text if self.comment else '',
            'Кем создано': self.creator,
            'Когда создано': moment(self.created_at).format('L'),
            'Кем изменено': self.editor,
            'Когда изменено': moment(self.edited_at).format('L')
        }
