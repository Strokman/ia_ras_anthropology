from pydantic import BaseModel as Base, ConfigDict


class CommentCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    text: str

    def __str__(self):
        return f'{self.text}'
