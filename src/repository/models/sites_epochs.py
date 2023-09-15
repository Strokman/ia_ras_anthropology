from src.repository import Column, ForeignKey, Integer, Table


sites_epochs = Table('sites_epochs',
                        Column("archaeological_site_id", Integer, ForeignKey("archaeological_sites.id")),
                        Column("epoch_id", Integer, ForeignKey("epochs.id"))
                        )