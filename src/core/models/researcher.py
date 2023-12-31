from pydantic import BaseModel as Base, ConfigDict


class ResearcherCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    affiliation: str
    middle_name: str | None

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name.capitalize()[0]}.{self.middle_name.capitalize()[0]}.'
        return f'{self.last_name} {self.first_name.capitalize()[0]}.'
