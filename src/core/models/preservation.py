from pydantic import BaseModel as Base, ConfigDict


class PreservationCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    description: str

    def __str__(self):
        return self.description
