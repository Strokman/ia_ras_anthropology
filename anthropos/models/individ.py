from anthropos import db
from .base_model import BaseModel
from .grave import Grave
from sqlalchemy.orm import Mapped


class Individ(db.Model, BaseModel):
    __tablename__ = 'individs'

    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(128))
    year = db.Column(db.Integer)
    age_min = db.Column(db.Integer)
    age_max = db.Column(db.Integer)
    type = db.Column(db.String(16))
    created_at = db.Column(db.DateTime, nullable=False)
    edited_at = db.Column(db.DateTime)
    sex_type = db.Column(db.String, db.ForeignKey('sex.sex'))
    # grave_id = db.Column(db.Integer, db.ForeignKey('graves.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('archaeological_sites.id'))
    created_by = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    edited_by = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    preservation_id = db.Column(db.Integer, db.ForeignKey('preservation.id'))

    site = db.relationship('ArchaeologicalSite', back_populates='individ')
    comment = db.relationship('Comment', uselist=False, back_populates='individ', cascade='all, delete-orphan')
    creator = db.relationship("DatabaseUser", foreign_keys='Individ.created_by', back_populates='individs_created')
    editor = db.relationship("DatabaseUser", foreign_keys='Individ.edited_by', back_populates='individs_edited')
    sex = db.relationship('Sex', back_populates='individ')
    preservation = db.relationship('Preservation', back_populates='individ')
    file = db.relationship('File', back_populates='individ', uselist=False, cascade='all, delete-orphan')
    grave = db.relationship('Grave', uselist=False, back_populates='individ', cascade='all, delete-orphan')

    def create_index(self):
        if self.grave.type == 'курганный':
            self.index = f'{self.site.name}-{self.year}-{self.grave.kurgan_number}-{self.grave.grave_number}'
        else:
            self.index = f'{self.site.name}-{self.year}-{self.grave.grave_number}'

    def __repr__(self):
        return {self.index}
