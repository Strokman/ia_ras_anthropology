from anthropos import db


sites_researchers = db.Table('sites_researchers',
                        db.Column("archaeological_site_id", db.Integer, db.ForeignKey("archaeological_sites.id")),
                        db.Column("researcher_id", db.Integer, db.ForeignKey("researchers.id"))
                        )