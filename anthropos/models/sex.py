from src.database import Column, relationship, Model, String
from src.database.base_model import BaseModel


class Sex(Model, BaseModel):
    __tablename__ = 'sex'

    sex = Column(String(16), primary_key=True)
    individs = relationship('Individ', back_populates='sex')

    def __init__(self, sex):
        self.sex = sex

    def __repr__(self):
        return self.sex
    