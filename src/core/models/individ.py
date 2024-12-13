from pydantic import BaseModel as Base, ConfigDict
from src.core.models.archaeological_site import ArchaeologicalSiteCore
from src.core.models.user import UserCore
from src.core.models.epoch import EpochCore
from src.core.models.sex import SexCore
from src.core.models.preservation import PreservationCore
from src.core.models.grave import GraveCore

from datetime import datetime


class IndividCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    index: str
    year: int
    age_min: int | None
    age_max: int | None
    age: str | None
    type: str
    created_at: datetime
    edited_at: datetime
    comment: str | None

    epoch: EpochCore | None
    sex: SexCore
    preservation: PreservationCore
    grave: GraveCore
    creator: UserCore
    editor: UserCore
    site: ArchaeologicalSiteCore

    def __str__(self):
        return f'{self.index}'
