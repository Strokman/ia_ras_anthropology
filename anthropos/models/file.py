from anthropos import db
from .base_model import BaseModel


class File(db.Model, BaseModel):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(128), nullable=False)
    filename = db.Column(db.String(128), nullable=False)
    extension = db.Column(db.String(36), nullable=False)
    individ_id = db.Column(db.Integer, db.ForeignKey('individs.id'))

    individ = db.relationship('Individ', back_populates='file')