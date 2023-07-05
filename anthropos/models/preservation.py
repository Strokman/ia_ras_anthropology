from anthropos import db
from .base_model import BaseModel


class Preservation(db.Model, BaseModel):
    __tablename__ = 'preservation'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))

    individ = db.relationship('Individ', back_populates='preservation')

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description