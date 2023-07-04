from anthropos import db
from .base_model import BaseModel


class Grave(db.Model, BaseModel):
    __tablename__ = 'graves'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32))
    catacomb = db.Column(db.Integer)
    chamber = db.Column(db.Integer)
    grave_number = db.Column(db.Integer)
    trench = db.Column(db.String(32))
    area = db.Column(db.String(32))
    object = db.Column(db.String(32))
    layer = db.Column(db.String(32))
    plast = db.Column(db.String(32))
    horizont = db.Column(db.String(32))
    square = db.Column(db.String(32))
    sector = db.Column(db.String(32))
    niveau_point = db.Column(db.Integer)
    tachymeter_point = db.Column(db.Integer)
    skeleton = db.Column(db.String(32))
    site_id = db.Column(db.Integer, db.ForeignKey('archaeological_sites.id'))

    individ = db.relationship('Individ', back_populates='grave')
    site = db.relationship('ArchaeologicalSite', back_populates='graves')

    def __repr__(self):
        return f'{self.site.name}/{self.grave_number}/{self.type}'