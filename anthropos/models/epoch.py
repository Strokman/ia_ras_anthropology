from anthropos import db
from .sites_epochs import sites_epochs
from .base_model import BaseModel


class Epoch(db.Model, BaseModel):
    __tablename__ = 'epochs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)

    sites = db.relationship('ArchaeologicalSite', secondary=sites_epochs, back_populates='epochs')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'
