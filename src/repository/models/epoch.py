from src.repository import Column, relationship, Model, Integer, String
from .sites_epochs import sites_epochs
from src.repository.base_model import BaseModel


class Epoch(Model, BaseModel):
    __tablename__ = 'epochs'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)

    individ = relationship('Individ', back_populates='epoch', cascade='all, delete-orphan')
    sites = relationship('ArchaeologicalSite', secondary=sites_epochs,
                                primaryjoin='Epoch.id==sites_epochs.c.epoch_id',
                             secondaryjoin='ArchaeologicalSite.id==sites_epochs.c.archaeological_site_id',
                        back_populates='epochs')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f'{self.name}'
