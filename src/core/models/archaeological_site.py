from pydantic import BaseModel as Base, ConfigDict
from src.core.models.region import RegionCore
from src.core.models.researcher import ResearcherCore
from typing import List


class ArchaeologicalSiteCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    long: float
    lat: float

    region: RegionCore
    researchers: List[ResearcherCore]

    def __str__(self):
        return self.name
