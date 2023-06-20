from anthropos import db


class Sex(db.Model):
    __tablename__ = 'sex'

    sex = db.Column(db.String(16), primary_key=True)
    individ = db.relationship('Individ', backref='sex')

    def __repr__(self):
        return f'Sex is {self.sex}'