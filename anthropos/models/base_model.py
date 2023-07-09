from flask_sqlalchemy.session import Session
from sqlalchemy import select


class BaseModel:

    @classmethod
    def get_all(cls, session: Session):
        return session.execute(select(cls)).scalars().all()

    def save_to_db(self, session: Session):
        session.add(self)
        session.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
