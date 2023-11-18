from pydantic import BaseModel as Base, ConfigDict


class UserCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    affiliation: str
    email: str
    middle_name: str | None

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'
        return f'{self.last_name} {self.first_name[0]}.'
