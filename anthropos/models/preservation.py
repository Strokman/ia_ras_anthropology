from src.database import Column, relationship, Model, Integer, String
from src.database.base_model import BaseModel


class Preservation(Model, BaseModel):
    __tablename__ = 'preservation'

    id = Column(Integer, primary_key=True)
    description = Column(String(64))

    individ = relationship('Individ', back_populates='preservation')

    def __init__(self, description):
        self.description = description

    def __repr__(self):
        return self.description