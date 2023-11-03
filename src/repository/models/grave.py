from src.repository import Column, relationship, ForeignKey, Model, Integer, String
from src.repository.base_model import BaseModel


class Grave(Model, BaseModel):
    __tablename__ = 'graves'

    id = Column(Integer, primary_key=True)
    grave_type = Column(String(32))
    kurgan_number = Column(String(32))
    grave_number = Column(Integer, nullable=False)
    catacomb = Column(String(32))
    chamber = Column(String(32))
    trench = Column(String(32))
    area = Column(String(32))
    object = Column(String(32))
    layer = Column(String(32))
    square = Column(String(32))
    sector = Column(String(32))
    niveau_point = Column(String(32))
    tachymeter_point = Column(String(64))
    skeleton = Column(String(32))
    individ_id = Column(Integer, ForeignKey('individs.id'))
    site_id = Column(Integer, ForeignKey('archaeological_sites.id'))

    individ = relationship('Individ', back_populates='grave')
    site = relationship('ArchaeologicalSite', back_populates='graves')

    def __repr__(self):
        if self.kurgan_number:
            return f'{self.site}, к.{self.kurgan_number}/п.{self.grave_number}'
        return f'{self.site}, п.{self.grave_number}'

    def __str__(self):
        desc = ', '.join([f'{k} {v}' for k, v in self.dict_russian().items() if v is not None])
        return desc

    def dict_russian(self):
         return {
            'к.': self.kurgan_number,
            'п.': self.grave_number,
            'катакомба': self.catacomb,
            'камера': self.chamber,
            'раскоп': self.trench,
            'участок': self.area,
            'объект': self.object,
            'слой': self.layer,
            'кв.': self.square,
            'сектор': self.sector,
            'нив. отметка': self.niveau_point,
            'тах. отметка': self.tachymeter_point,
            'скелет': self.skeleton
        }