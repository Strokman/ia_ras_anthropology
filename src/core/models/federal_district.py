from pydantic import BaseModel as Base, ConfigDict


class FedDistrCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
