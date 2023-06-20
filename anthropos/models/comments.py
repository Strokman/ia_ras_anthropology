from anthropos import db

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)

    individ = db.relationship('Individ', back_populates='comment')
