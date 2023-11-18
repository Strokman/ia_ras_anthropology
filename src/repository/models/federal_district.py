from src.repository import Column, relationship, Model, Integer, String
from src.repository.base_model import BaseModel



class FederalDistrict(Model, BaseModel):
    __tablename__ = 'federal_districts'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    region = relationship('Region', back_populates='federal_district')

    def __repr__(self):
        return f'{self.name} федеральный округ'