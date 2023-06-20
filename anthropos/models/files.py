from anthropos import db


class File(db.Model):
    __tablename__ = 'files'

    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(128), nullable=False)

    individ = db.relationship('Individ', back_populates='file')