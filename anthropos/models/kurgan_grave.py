from anthropos import db
from .base_model import BaseModel


class KurganGrave(db.Model, BaseModel):
    __tablename__ = 'kurgan_graves'

    id = db.Column(db.Integer, primary_key=True)
    kurgan_number = db.Column(db.Integer)
    grave_number = db.Column(db.Integer)
    catacomb = db.Column(db.Integer)
    chamber = db.Column(db.Integer)
    niveau_point = db.Column(db.Integer)
    tachymeter_point = db.Column(db.Integer)
    skeleton = db.Column(db.String(32))
    site_id = db.Column(db.Integer, db.ForeignKey('archaeological_sites.id'))

    individ = db.relationship('Individ', back_populates='grave')
    site = db.relationship('ArchaeologicalSite', back_populates='graves')

    def __repr__(self):
        return f'{self.grave_number}'