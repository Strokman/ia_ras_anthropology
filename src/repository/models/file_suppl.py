from src.repository import Column, ForeignKey, relationship, Model, Integer, String
from src.repository.base_model import BaseModel


class SupplementaryFile(Model, BaseModel):
    __tablename__ = 'supplementary_files'

    id = Column(Integer, primary_key=True)
    filename = Column(String(128), nullable=False)
    extension = Column(String(36), nullable=False)
    original_filename = Column(String(128), nullable=False)
    object_storage_key = Column(String(256), nullable=False)
    site_id = Column(Integer, ForeignKey('archaeological_sites.id'))

    site = relationship('ArchaeologicalSite', back_populates='supplementary_file')

    def __repr__(self):
        return f'{self.site}-suppl{self.extension}'
