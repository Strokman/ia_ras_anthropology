from pydantic import BaseModel as Base, ConfigDict
from src.core.models.federal_district import FedDistrCore


class RegionCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    federal_district: FedDistrCore



