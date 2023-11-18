from pydantic import BaseModel as Base, ConfigDict


class SexCore(Base):
    model_config = ConfigDict(from_attributes=True)

    sex: str

    def __str__(self):
        return self.sex
