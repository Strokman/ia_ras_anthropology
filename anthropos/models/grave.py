from anthropos import db
from .base_model import BaseModel


class Grave(db.Model, BaseModel):
    __tablename__ = 'graves'

    id = db.Column(db.Integer, primary_key=True)
    grave_type = db.Column(db.String(32))
    kurgan_number = db.Column(db.String(32))
    grave_number = db.Column(db.Integer)
    catacomb = db.Column(db.Integer)
    chamber = db.Column(db.Integer)
    trench = db.Column(db.String(32))
    area = db.Column(db.String(32))
    object = db.Column(db.String(32))
    layer = db.Column(db.String(32))
    square = db.Column(db.String(32))
    sector = db.Column(db.String(32))
    niveau_point = db.Column(db.Integer)
    tachymeter_point = db.Column(db.Integer)
    skeleton = db.Column(db.String(32))
    individ_id = db.Column(db.Integer, db.ForeignKey('individs.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('archaeological_sites.id'))

    individ = db.relationship('Individ', back_populates='grave')
    site = db.relationship('ArchaeologicalSite', back_populates='graves')

    def __repr__(self):
        if self.kurgan_number:
            return f'к.{self.kurgan_number}/п.{self.grave_number}'
        return f'п.{self.grave_number}'
    
    def __str__(self):
        desc = ', '.join([f'{k} {v}' for k, v in self.dict_russian().items() if v is not None])
        return desc
    
    def dict_russian(self):
        attrs = {
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
        return attrs