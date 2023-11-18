from src.repository import Column, relationship, Model, Integer, String
from src.repository.base_model import BaseModel
from src.repository.models.sites_researchers import sites_researchers

# from src.repository.models import ArchaeologicalSite

from pydantic import BaseModel as Base, ConfigDict


class Researcher1(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    affiliation: str
    middle_name: str | None
    # sites: list[ArchaeologicalSite] | None


class Researcher(BaseModel, Model):
    __tablename__ = 'researchers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    affiliation = Column(String(128), nullable=False)
    middle_name = Column(String(128))

    sites = relationship('ArchaeologicalSite', secondary=sites_researchers,
                         primaryjoin='Researcher.id==sites_researchers.c.researcher_id',
                         secondaryjoin='ArchaeologicalSite.id==sites_researchers.c.archaeological_site_id',
                         back_populates='researchers')

    @property
    def serialize(self):
        return Researcher1.model_validate(self)

    def __repr__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name.capitalize()[0]}.{self.middle_name.capitalize()[0]}.'
        return f'{self.last_name} {self.first_name.capitalize()[0]}.'
