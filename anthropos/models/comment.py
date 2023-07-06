from anthropos import db
from .base_model import BaseModel

class Comment(db.Model, BaseModel):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    invidiv_id = db.Column(db.Integer, db.ForeignKey('individs.id'))


    individ = db.relationship('Individ', back_populates='comment')
