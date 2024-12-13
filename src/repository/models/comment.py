# from src.repository import Column, relationship, ForeignKey, Model, String, Integer
# from src.repository.base_model import BaseModel


# class Comment(Model, BaseModel):
#     __tablename__ = 'comments'

#     id = Column(Integer, primary_key=True)
#     text = Column(String, nullable=False)
#     invidiv_id = Column(Integer, ForeignKey('individs.id'))

#     individ = relationship('Individ', back_populates='comment')

#     def __repr__(self):
#         return f'{self.text}'
