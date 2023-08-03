from anthropos import db
from .base_model import BaseModel


class Sex(db.Model, BaseModel):
    __tablename__ = 'sex'

    sex = db.Column(db.String(16), primary_key=True)
    individs = db.relationship('Individ', back_populates='sex')

    def __init__(self, sex):
        self.sex = sex

    def __repr__(self):
        return self.sex
    