from pydantic import BaseModel as Base, ConfigDict


class GraveCore(Base):
    model_config = ConfigDict(from_attributes=True)

    id: int
    grave_type: str | None
    kurgan_number: str | None
    grave_number: int
    catacomb: str | None
    chamber: str | None
    trench: str | None
    area: str | None
    object: str | None
    layer: str | None
    square: str | None
    sector: str | None
    niveau_point: str | None
    tachymeter_point: str | None
    skeleton: str | None

    def __str__(self):
        desc = ', '.join([f'{k} {v}' for k, v in self.dict_russian().items() if v is not None])
        return desc

    def dict_russian(self):
        return {
            'к.': self.kurgan_number,
            'п.': self.grave_number,
            'катакомба': self.catacomb,
            'камера': self.chamber,
            'раскоп': self.trench,
            'участок': self.area,
            'объект': self.object,
            'слой': self.layer,
            'кв.': self.square,
            'сектор': self.sector,
            'нив. отметка': self.niveau_point,
            'тах. отметка': self.tachymeter_point,
            'скелет': self.skeleton
        }