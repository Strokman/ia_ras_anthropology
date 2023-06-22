from anthropos import db
from .base_model import BaseModel


class Researcher(db.Model, BaseModel):
    __tablename__ = 'researchers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128))

    sites = db.relationship('ArchaeologicalSite', back_populates='researcher')

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    def __init__(self, first_name, last_name, middle_name=None):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name.capitalize()[0]}.{self.middle_name.capitalize()[0]}.'
        return f'{self.last_name} {self.first_name.capitalize()[0]}.'

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'
