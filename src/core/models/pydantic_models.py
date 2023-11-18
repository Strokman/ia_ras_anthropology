# from src.repository.models import FederalDistrict
# from src.repository.models import Region
from pydantic import BaseModel as Base, ConfigDict
from typing import Type, List
from core.models.federal_district import FedDistrClass

class RegionClass(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    federal_district: FedDistrClass



