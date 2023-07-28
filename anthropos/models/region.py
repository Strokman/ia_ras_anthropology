from anthropos import db
from .base_model import BaseModel


class Region(db.Model, BaseModel):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    federal_districts_id = db.Column(db.ForeignKey('federal_districts.id'))

    federal_district = db.relationship('FederalDistrict', back_populates='region')
    sites = db.relationship('ArchaeologicalSite', back_populates='regions')

    def __repr__(self):
        return f'{self.name}'