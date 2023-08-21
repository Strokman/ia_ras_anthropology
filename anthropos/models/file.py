from src.database import Column, ForeignKey, relationship, Model, Integer, String
from src.database.base_model import BaseModel


class File(Model, BaseModel):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    path = Column(String(128), nullable=False)
    filename = Column(String(128), nullable=False)
    extension = Column(String(36), nullable=False)
    individ_id = Column(Integer, ForeignKey('individs.id'))

    individ = relationship('Individ', back_populates='file')