from anthropos.extensions import db
from anthropos.models.base_model import BaseModel
from anthropos.models.sites_researchers import sites_researchers


class Researcher(db.Model, BaseModel):
    __tablename__ = 'researchers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    affiliation = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128))

    sites = db.relationship('ArchaeologicalSite', secondary=sites_researchers,
                                  primaryjoin='ArchaeologicalSite.id==sites_researchers.c.archaeological_site_id',
                                  secondaryjoin='Researcher.id==sites_researchers.c.researcher_id',
                                  back_populates='researchers')

    def __repr__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name.capitalize()[0]}.{self.middle_name.capitalize()[0]}.'
        return f'{self.last_name} {self.first_name.capitalize()[0]}.'
