from sqlalchemy import select
from sqlalchemy.orm.scoping import scoped_session


class BaseModel:

    @classmethod
    def get_all(cls, session: scoped_session):
        return session.execute(select(cls)).scalars().all()
        # return session.scalars(select(cls))

    def save_to_db(self, session: scoped_session):
        session.add(self)
        session.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
