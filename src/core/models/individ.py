from pydantic import BaseModel as Base, ConfigDict
from src.core.models.archaeological_site import ArchaeologicalSiteCore

from datetime import datetime


class IndividCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    index: str
    year: int
    age_min: int | None
    age_max: int | None
    type: str
    created_at: datetime
    edited_at: datetime

    site: ArchaeologicalSiteCore
