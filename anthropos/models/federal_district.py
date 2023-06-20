from anthropos import db


class FederalDistrict(db.Model):
    __tablename__ = 'federal_districts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    region = db.relationship('Region', back_populates='federal_district')

    def __repr__(self):
        return f'{self.name} федеральный округ'