from anthropos import db


class Individ(db.Model):
    __tablename__ = 'individs'

    id = db.Column(db.Integer, primary_key=True)
    index = db.Column(db.String(128))
    year = db.Column(db.Integer)
    age_min = db.Column(db.Integer)
    age_max = db.Column(db.Integer)
    sex_type = db.Column(db.String, db.ForeignKey('sex.sex'))
    grave_id = db.Column(db.Integer, db.ForeignKey('graves.id'))
    site_id = db.Column(db.Integer, db.ForeignKey('archaeological_sites.id'))
    created_by = db.Column(db.Integer, db.ForeignKey("database_users.id"))
    # comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    # preservation_id = db.Column(db.Integer, db.ForeignKey('preservation.id'))
    # file_id = db.Column(db.Integer, db.ForeignKey('files.id'))

    # site = db.relationship('ArchaeologicalSite', back_populates='individ')
    # comment = db.relationship('Comment', back_populates='individ')
    # creator = db.relationship("DatabaseUser", back_populates='individs')
    # sex = db.relationship('Sex', backref='individ')
    # preservation = db.relationship('Preservation', back_populates='individ')
    # file = db.relationship('File', back_populates='individ')
    # burial_type = db.relationship('BurialType', back_populates='individ')

    def create_index(self, site):
        self.index = f'{site.name}-{self.year}'

    def __repr__(self):
        return f'{self.index}:{self.sex}:{self.age_min}-{self.age_max}'