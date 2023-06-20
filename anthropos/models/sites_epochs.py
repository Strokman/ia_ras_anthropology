from anthropos import db


sites_epochs = db.Table('sites_epochs',
                        db.Column("archaeological_site_id", db.Integer, db.ForeignKey("archaeological_sites.id")),
                        db.Column("epoch_id", db.Integer, db.ForeignKey("epochs.id"))
                        )