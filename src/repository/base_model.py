"""
Module contains Base model, which implements basic CRUD operations.
This model is inherited by most of all other SQLAlchemy models in
the Base Habilis app.
"""
from typing import Self

from flask import current_app
from flask_login import current_user
from sqlalchemy import select
from sqlalchemy.orm import scoped_session

from src.repository import session


class BaseModel:

    @classmethod
    def create(cls, **kwargs: dict) -> Self:
        """
        Create a new record and save it in the database.

        Returns:
            Instance of a class
        """
        instance = cls()
        for attr, value in kwargs.items():
            if hasattr(cls, attr):
                setattr(instance, attr, value)
        instance.save()
        return instance

    @classmethod
    def get_by_id(cls, id: int | str):
        """
        get_by_id method takes an id as argument and returns
        instance of a class = entry in the DB

        Args:
            id (int | str): id of the record from the DB

        Returns:
            Self: entry from DB, instance of a class
        """
        return session.get(cls, id)

    @classmethod
    def get_all(cls, attr: str = None) -> list[Self]:
        if attr and hasattr(cls, attr):
            stmt = select(cls).order_by(getattr(cls, attr))
        elif hasattr(cls, 'name'):
            stmt = select(cls).order_by(cls.name)
        else:
            stmt = select(cls).order_by(cls.id)
        result = session.scalars(stmt).all()
        return result

    @classmethod
    def get_one_by_attr(cls,  attr: str, repo: scoped_session, value):
        if hasattr(cls, attr):
            stmt = select(cls).where(getattr(cls, attr) == value)
            result = repo.scalar(stmt)
        return result
    

    def save(self, commit: bool = True):
        """Save the record."""
        session.add(self)
        if commit:
            session.commit()
        return self

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            if hasattr(self, attr):
                setattr(self, attr, value)
        if commit:
            return self.save()
        return self

    def delete(self, commit: bool = True) -> None:
        """Remove the record from the database."""
        session.delete(self)
        if commit:
            return session.commit()
        return

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
