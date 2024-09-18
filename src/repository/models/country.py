from src.repository import Column, relationship, Model, Integer, String
from src.repository.base_model import BaseModel


class Country(Model, BaseModel):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    region = relationship('Region', back_populates='country', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.name}'
