from anthropos import db


class Preservation(db.Model):
    __tablename__ = 'preservation'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(64))

    individ = db.relationship('Individ', back_populates='preservation')

    def __init__(self, description):
        self.description = description