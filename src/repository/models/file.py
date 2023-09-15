from src.repository import Column, ForeignKey, relationship, Model, Integer, String
from src.repository.base_model import BaseModel


class File(Model, BaseModel):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(128), nullable=False)
    extension = Column(String(36), nullable=False)
    individ_id = Column(Integer, ForeignKey('individs.id'))

    individ = relationship('Individ', back_populates='file')

    def __repr__(self):
        return f'{self.individ.index}.{self.extension}'
