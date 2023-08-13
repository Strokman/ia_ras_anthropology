from anthropos.extensions import login, db
from werkzeug.security import check_password_hash, generate_password_hash
from .base_model import BaseModel
from flask_login import UserMixin
from flask import url_for, flash, session, redirect, current_app, render_template
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from anthropos.lib.email import send_email
import jwt
from time import time
from functools import wraps


class DatabaseUser(UserMixin, db.Model, BaseModel):
    __tablename__: str = 'database_users'

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

    sites_created = db.relationship('ArchaeologicalSite', foreign_keys='ArchaeologicalSite.created_by', back_populates='creator')
    sites_edited = db.relationship('ArchaeologicalSite', foreign_keys='ArchaeologicalSite.edited_by', back_populates='editor')
    individs_created = db.relationship('Individ', foreign_keys='Individ.created_by', back_populates='creator')
    individs_edited = db.relationship('Individ', foreign_keys='Individ.edited_by', back_populates='editor')

    def __init__(self,
                 username,
                 password,
                 first_name,
                 last_name,
                 affiliation,
                 email,
                 created,
                 last_login,
                 middle_name=None) -> None:
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.affiliation = affiliation
        self.email = email
        self.created = created
        self.last_login = last_login
        self.middle_name = middle_name

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def send_confirmation_email(self) -> None:
        link = current_app.config['HOST'] + url_for('auth.user_confirmation', username=self.username, token=self.token)
        send_email('BaseHabilis - подтверждение email',
                   sender=current_app.config['ADMIN_EMAIL'],
                   recipients=[self.email],
                   html_body=render_template('email/mail_confirmation.html',
                                             link=link))


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')
    

    def send_password_reset_email(self):
        link = current_app.config['HOST'] + url_for('auth.reset_password', token=self.get_reset_password_token())
        send_email('BaseHabilis - сброс пароля',
               sender=current_app.config['ADMIN_EMAIL'],
               recipients=[self.email],
               text_body=render_template('email/reset_password.txt',
                                         user=self, link=link),
               html_body=render_template('email/reset_password.html',
                                         user=self, link=link))

    def is_admin(self) -> bool:
        return self.role == 'admin'

    def is_active(self) -> bool:
        return self.activated

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        user: DatabaseUser | None = DatabaseUser.get_one_by_attr(DatabaseUser.id, id)
        return user

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name[0]}.{self.middle_name[0]}.'
        return f'{self.last_name} {self.first_name[0]}.'

    def __repr__(self):
        return f'{self.id}: {self.username}'


@login.user_loader
def load_user(user_id):
    user = db.session.query(DatabaseUser).get(int(user_id))
    if not user or not user.is_active():
        return None
    return user


def admin_required(f):
    @wraps(f)
    def decorated_view(*args, **kwargs):
        if session['user_role'] != 'admin':
            flash('Недостаточно прав', 'warning')
            return redirect(url_for('index.index'))
        else:
            return f(*args, **kwargs)
    return decorated_view


