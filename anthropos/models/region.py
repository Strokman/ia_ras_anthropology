from anthropos import db


class Region(db.Model):
    __tablename__ = 'regions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    federal_district_id = db.Column(db.ForeignKey('federal_districts.id'))

    federal_district = db.relationship('FederalDistrict', back_populates='region')
    sites = db.relationship('ArchaeologicalSite', back_populates='regions')

    # individ = relationship('Individ', back_populates='region')

    def __repr__(self):
        return f'{self.name} part of {self.federal_district}'