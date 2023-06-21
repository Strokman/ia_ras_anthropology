from anthropos import db
from anthropos.models.sites_epochs import sites_epochs
# from anthropos.models import DatabaseUser, Region, Researcher


class ArchaeologicalSite(db.Model):
    __tablename__ = 'archaeological_sites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    long = db.Column(db.Numeric(9, 6), nullable=False)
    lat = db.Column(db.Numeric(9, 6), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    editor_id = db.Column(db.Integer, db.ForeignKey('database_users.id'))
    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.id"))
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))

    owner = db.relationship("DatabaseUser", foreign_keys="ArchaeologicalSite.creator_id", back_populates='sites_created')
    editor = db.relationship("DatabaseUser", foreign_keys="ArchaeologicalSite.editor_id", back_populates='sites_edited')
    epochs = db.relationship("Epoch", secondary=sites_epochs, back_populates='sites')
    researcher = db.relationship("Researcher", back_populates='sites')
    regions = db.relationship('Region', back_populates='sites')
    individ = db.relationship("Individ", back_populates='site')

    def __init__(self, name: str, long: float, lat: float, user, researcher, region):
        self.name = name
        self.long = long
        self.lat = lat
        self.creator_id = user.id
        self.editor_id = user.id
        self.researcher_id = researcher.id
        self.region_id = region.id

    def __repr__(self):
        return f'{self.name} - {self.regions}'
