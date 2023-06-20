from anthropos import db
from anthropos.models.sites_epochs import sites_epochs


class ArchaeologicalSite(db.Model):
    __tablename__ = 'archaeological_sites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    long = db.Column(db.Numeric(9, 6), nullable=False)
    lat = db.Column(db.Numeric(9, 6), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    edited_by = db.Column(db.Integer, db.ForeignKey('database_users.id'))
    researcher_id = db.Column(db.Integer, db.ForeignKey("researchers.id"))
    # region_id = db.Column(db.Integer, db.ForeignKey('regions.id'))

    creator = db.relationship("DatabaseUser", foreign_keys="ArchaeologicalSite.created_by", backref='creator')
    editor = db.relationship("DatabaseUser", foreign_keys="ArchaeologicalSite.edited_by", backref='editor')
    epochs = db.relationship("Epoch", secondary=sites_epochs, backref='sites')
    researcher = db.relationship("Researcher", backref='researchers')
    # regions = db.relationship('Region', back_populates='sites')
    # individ = db.relationship("Individ", back_populates='site')

    def __init__(self, name, long, lat, created_by, edited_by):
        self.name = name
        self.long = long
        self.lat = lat
        self.created_by = created_by
        self.edited_by = edited_by

    def __repr__(self):
        return f'{self.name} - {self.regions}'
