from sqlalchemy import select
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.attributes import InstrumentedAttribute


class BaseModel:

    @classmethod
    def get_all(cls, session: scoped_session, attr: InstrumentedAttribute=None):
        if attr:
            stmt = select(cls).order_by(attr)
        else:
            stmt = select(cls).order_by(cls.name)
        res = session.execute(stmt).scalars().all()
        return res

    def save_to_db(self, session: scoped_session):
        session.add(self)
        session.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
