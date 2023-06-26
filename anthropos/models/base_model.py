from flask_sqlalchemy.session import Session


class BaseModel:

    @classmethod
    def get_all(cls, db: Session):
        return db.query(cls).all()

    def save_to_db(self, db: Session):
        db.add(self)
        db.commit()

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
