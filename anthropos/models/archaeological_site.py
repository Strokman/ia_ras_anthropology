from anthropos import db
from anthropos.models.sites_epochs import sites_epochs
from .base_model import BaseModel
# from anthropos.models import DatabaseUser, Region, Researcher


class ArchaeologicalSite(db.Model, BaseModel):
    __tablename__ = 'archaeological_sites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    long = db.Column(db.Numeric(9, 6), nullable=False)
    lat = db.Column(db.Numeric(9, 6), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    editor_id = db.Column(db.Integer, db.ForeignKey('database_users.id'))
    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.id", ondelete='CASCADE'))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))

    creator = db.relationship("DatabaseUser", foreign_keys="ArchaeologicalSite.creator_id", back_populates='sites_created')
    editor = db.relationship("DatabaseUser", foreign_keys="ArchaeologicalSite.editor_id", back_populates='sites_edited')
    epochs = db.relationship("Epoch", secondary=sites_epochs,
                             primaryjoin='ArchaeologicalSite.id==sites_epochs.c.archaeological_site_id',
        secondaryjoin= 'Epoch.id==sites_epochs.c.epoch_id',
          back_populates='sites')
    researcher = db.relationship("Researcher", back_populates='sites')
    regions = db.relationship('Region', back_populates='sites')
    individ = db.relationship("Individ", back_populates='site')
    graves = db.relationship("Grave", back_populates='site')

    def __init__(self, name: str, long: float, lat: float, user, researcher, region_id):
        self.name = name
        self.long = long
        self.lat = lat
        self.creator_id = user.id
        self.editor_id = user.id
        self.researcher_id = researcher.id
        self.region_id = region_id

    def __repr__(self):
        return self.name
