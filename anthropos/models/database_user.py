from anthropos import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin


class DatabaseUser(UserMixin, db.Model):
    __tablename__ = 'database_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128))
    affiliation = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), index=True, nullable=False, unique=True)
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

    def __init__(self, username, password, first_name, last_name, affiliation, email, created, last_login, middle_name=None):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.affiliation = affiliation
        self.email = email
        self.created = created
        self.last_login = last_login
        self.middle_name: str = middle_name

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name.capitalize()[0]}.{self.middle_name.capitalize()[0]}.'
        return f'{self.last_name} {self.first_name.capitalize()[0]}.'

    def __repr__(self):
        return f'{self.id}: {self.username}'


@login.user_loader
def load_user(user_id):
    return db.session.query(DatabaseUser).get(int(user_id))
