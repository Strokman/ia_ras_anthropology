from src.repository import Column, relationship, ForeignKey, Model, Integer, String
from src.repository.base_model import BaseModel


class Region(Model, BaseModel):
    __tablename__ = 'regions'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    federal_districts_id = Column(ForeignKey('federal_districts.id'))
    country_id = Column(ForeignKey('countries.id'))

    country = relationship('Country', back_populates='region')
    federal_district = relationship('FederalDistrict', back_populates='region')
    sites = relationship('ArchaeologicalSite', back_populates='region')

    def __repr__(self):
        return f'{self.name}'
