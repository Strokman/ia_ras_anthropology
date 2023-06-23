from anthropos import db


class BaseModel:

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
