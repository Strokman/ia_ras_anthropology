from anthropos import db
from anthropos.models.sites_epochs import sites_epochs
from anthropos.models.sites_researchers import sites_researchers
from .base_model import BaseModel


class ArchaeologicalSite(db.Model, BaseModel):
    __tablename__ = 'archaeological_sites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    long = db.Column(db.Numeric(9, 6), nullable=False)
    lat = db.Column(db.Numeric(9, 6), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    edited_by = db.Column(db.Integer, db.ForeignKey('database_users.id'))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))

    creator = db.relationship("DatabaseUser", foreign_keys="ArchaeologicalSite.created_by", back_populates='sites_created')
    editor = db.relationship("DatabaseUser", foreign_keys="ArchaeologicalSite.edited_by", back_populates='sites_edited')
    region = db.relationship('Region', back_populates='sites')
    individs = db.relationship("Individ", back_populates='site')
    graves = db.relationship("Grave", back_populates='site')

    epochs = db.relationship("Epoch", secondary=sites_epochs,
                             primaryjoin='ArchaeologicalSite.id==sites_epochs.c.archaeological_site_id',
                             secondaryjoin='Epoch.id==sites_epochs.c.epoch_id',
                             back_populates='sites')
    researchers = db.relationship("Researcher", secondary=sites_researchers,
                                  primaryjoin='ArchaeologicalSite.id==sites_researchers.c.archaeological_site_id',
                                  secondaryjoin='Researcher.id==sites_researchers.c.researcher_id',
                                  back_populates='sites')

    def __repr__(self):
        return self.name
