from pydantic import BaseModel as Base, ConfigDict


class ResearcherCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    affiliation: str
    middle_name: str | None