from pydantic import BaseModel as Base, ConfigDict
from src.core.models.country import CountryCore


class RegionCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    country: CountryCore

    def __str__(self):
        return f'{self.name}'


