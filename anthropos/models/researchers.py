from anthropos import db


class Researcher(db.Model):
    __tablename__ = 'researchers'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128), nullable=False)
    last_name = db.Column(db.String(128), nullable=False)
    middle_name = db.Column(db.String(128))

    sites = db.relationship('ArchaeologicalSite', backref='sites')

    def __str__(self):
        if self.middle_name:
            return f'{self.last_name} {self.first_name.capitalize()[0]}.{self.middle_name.capitalize()[0]}.'
        return f'{self.last_name} {self.first_name.capitalize()[0]}.'

    def __repr__(self):
        return f'{self.first_name} {self.last_name}'