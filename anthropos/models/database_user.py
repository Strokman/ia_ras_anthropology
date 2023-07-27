from anthropos.extensions import login, db
from werkzeug.security import check_password_hash, generate_password_hash
from .base_model import BaseModel
from flask_login import UserMixin
from flask import request, url_for, flash, session, redirect, current_app
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from anthropos.lib import MailgunEngine
import jwt
from time import time
from functools import wraps


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

    individs_created = db.relationship('Individ', foreign_keys='Individ.created_by', back_populates='creator')
    individs_edited = db.relationship('Individ', foreign_keys='Individ.edited_by', back_populates='editor')
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
        link = request.url_root[:-1] + url_for('auth.user_confirmation', username=self.username, token=self.token)
        MailgunEngine.send_confirmation_email(self.email, link)

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

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return db.session.query(DatabaseUser).filter_by(id=id)

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
        flash('Email is not confirmed')
        return None
    return user


def admin_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if session['user_role'] != 'admin':
            flash('Unauthorized access', 'warning')
            return redirect(url_for('index.index'))
        else:
            return f(*args, **kwargs)
    return decorated_view


