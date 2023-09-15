from src.repository import Column, relationship, Model, Integer, String
from src.repository.base_model import BaseModel
from src.repository.models.sites_researchers import sites_researchers


class Researcher(BaseModel, Model):
    __tablename__ = 'researchers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    affiliation = Column(String(128), nullable=False)
    middle_name = Column(String(128))

    sites = relationship('ArchaeologicalSite', secondary=sites_researchers,
                            back_populates='researchers')

    # почему-то не работает, проверить, если добавляю в релейшн
    # primaryjoin='ArchaeologicalSite.id==sites_researchers.c.archaeological_site_id',
    #   secondaryjoin='Researcher.id==sites_researchers.c.researcher_id',

    def __repr__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name.capitalize()[0]}.{self.middle_name.capitalize()[0]}.'
        return f'{self.last_name} {self.first_name.capitalize()[0]}.'
