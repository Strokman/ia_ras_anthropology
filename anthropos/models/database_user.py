from anthropos import db, login, app
from werkzeug.security import check_password_hash, generate_password_hash
from .base_model import BaseModel
from flask_login import UserMixin
from flask import request, url_for, flash
from requests import post
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from anthropos.mail_text import create_text


class DatabaseUser(UserMixin, db.Model, BaseModel):
    __tablename__ = 'database_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128))
    affiliation = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), index=True, nullable=False, unique=True)
    activated = db.Column(db.Boolean, nullable=False, default=False)
    role = db.Column(db.String(16), nullable=False, default='user')
    token = db.Column(UUID(as_uuid=True), nullable=False, default=uuid4())
    created = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=False)

    individs = db.relationship('Individ', back_populates='creator')
    """
    РЕЛЕЙШЕНЫ ПИСАТЬ КАК ЗДЕСЬ И В КЛАССЕ АРХПАМЯТНИК - ТОГДА РАБОТАЕТ НОРМАЛЬНО
    """
    sites_created = db.relationship('ArchaeologicalSite',
                                    foreign_keys='ArchaeologicalSite.creator_id',
                                    back_populates='owner')
    sites_edited = db.relationship('ArchaeologicalSite', foreign_keys='ArchaeologicalSite.editor_id',
                                    back_populates='editor')

    def __init__(self,
                 username,
                 password,
                 first_name,
                 last_name,
                 affiliation,
                 email,
                 created,
                 last_login,
                 middle_name=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.affiliation = affiliation
        self.email = email
        self.created = created
        self.last_login = last_login
        self.middle_name: str = middle_name

    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('user_confirmation', username=self.username, token=self.token)

        return post(f'https://api.mailgun.net/v3/{app.config["MAILGUN_DOMAIN"]}/messages',
                    auth=('api', app.config['MAILGUN_API_KEY']),
                    data={
                        'from': f'Anton Strokov <mailgun@{app.config["MAILGUN_DOMAIN"]}>',
                        'to': self.email,
                        'subject': 'Registration confirmation',
                        'html': create_text(link)
                    })

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def activate_user(cls, user_id: int):
        user = db.session.query(cls).filter_by(id=user_id).first()
        if not user:
            return f'There is no user {user.username}'
        user.activated = True
        db.session.commit()
        return f'User {user.username} is active'

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name.capitalize()[0]}.{self.middle_name.capitalize()[0]}.'
        return f'{self.last_name} {self.first_name.capitalize()[0]}.'

    def __repr__(self):
        return f'{self.id}: {self.username}'


@login.user_loader
def load_user(user_id):
    user = db.session.query(DatabaseUser).get(int(user_id))
    if not user:
        return None
    elif not user.activated:
        flash('Email is not confiremd')
        return None
    return user
