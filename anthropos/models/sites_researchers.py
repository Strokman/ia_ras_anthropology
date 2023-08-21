from src.database import Column, ForeignKey, Table, Integer


sites_researchers = Table('sites_researchers',
                        Column("archaeological_site_id", Integer, ForeignKey("archaeological_sites.id")),
                        Column("researcher_id", Integer, ForeignKey("researchers.id"))
                        )