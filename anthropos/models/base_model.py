from sqlalchemy import select
from sqlalchemy.orm.scoping import scoped_session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from anthropos.extensions import db


class BaseModel:

    @classmethod
    def get_all(cls, attr: InstrumentedAttribute=None):
        if attr:
            stmt = select(cls).order_by(attr)
        else:
            stmt = select(cls).order_by(cls.name)
        res = db.session.execute(stmt).scalars().all()
        return res
    
    @classmethod
    def get_one_by_attr(cls, attr, value):
        stmt = select(cls).where(attr==value)
        res = db.session.scalar(stmt)
        return res

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
