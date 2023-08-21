from src.database import Column, ForeignKey, relationship, Model, Numeric, String, Integer
from anthropos.models.sites_epochs import sites_epochs
from anthropos.models.sites_researchers import sites_researchers
from src.database.base_model import BaseModel


class ArchaeologicalSite(Model, BaseModel):
    __tablename__: str = 'archaeological_sites'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, index=True)
    long = Column(Numeric(9, 6), nullable=False)
    lat = Column(Numeric(9, 6), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"))
    edited_by = Column(Integer, ForeignKey('users.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))

    creator = relationship("User", foreign_keys="ArchaeologicalSite.created_by", back_populates='sites_created')
    editor = relationship("User", foreign_keys="ArchaeologicalSite.edited_by", back_populates='sites_edited')
    region = relationship('Region', back_populates='sites')
    individs = relationship("Individ", back_populates='site', cascade='all, delete-orphan')
    graves = relationship("Grave", back_populates='site', cascade='all, delete-orphan')

    epochs = relationship("Epoch", secondary=sites_epochs,
                             primaryjoin='ArchaeologicalSite.id==sites_epochs.c.archaeological_site_id',
                             secondaryjoin='Epoch.id==sites_epochs.c.epoch_id',
                             back_populates='sites')
    researchers = relationship("Researcher", secondary=sites_researchers,
                                  primaryjoin='ArchaeologicalSite.id==sites_researchers.c.archaeological_site_id',
                                  secondaryjoin='Researcher.id==sites_researchers.c.researcher_id',
                                  back_populates='sites')

    def __repr__(self):
        return self.name
