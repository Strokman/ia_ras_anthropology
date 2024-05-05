from pydantic import BaseModel as Base, ConfigDict


class CountryCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str

    def __str__(self):
        return f'{self.name}'
