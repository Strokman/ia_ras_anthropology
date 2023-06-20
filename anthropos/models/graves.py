from anthropos import db


class Grave(db.Model):
    __tablename__ = 'graves'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)
    catacomb = db.Column(db.Integer)
    chamber = db.Column(db.Integer)
    grave_number = db.Column(db.Integer)
    trench = db.Column(db.String(32))
    area = db.Column(db.String(32))
    object = db.Column(db.String(32))
    layer = db.Column(db.String(32))
    plast = db.Column(db.String(32))
    horizont = db.Column(db.String(32))
    square = db.Column(db.String(32))
    sector = db.Column(db.String(32))
    niveau_point = db.Column(db.Integer)
    tachymeter_point = db.Column(db.Integer)
    skeleton = db.Column(db.String(32))

    individ = db.relationship('Individ', backref='grave')

    # def __repr__(self):
    #     return f'Kurgan {self.number}, grave {self.grave_number}'