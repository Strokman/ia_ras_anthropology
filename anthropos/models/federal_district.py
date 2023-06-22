from anthropos import db
from .base_model import BaseModel


class FederalDistrict(db.Model, BaseModel):
    __tablename__ = 'federal_districts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    region = db.relationship('Region', back_populates='federal_district')

    def __repr__(self):
        return f'{self.name} федеральный округ'