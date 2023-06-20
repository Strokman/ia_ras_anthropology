from anthropos import db, app
from anthropos.models.epochs import Epoch
from anthropos.models.user import DatabaseUser
from anthropos.models.sites import ArchaeologicalSite
from anthropos.models.sites_epochs import sites_epochs
from anthropos.models.sex import Sex
from anthropos.models.individs import Individ
from anthropos.models.graves import Grave
from anthropos.models.researchers import Researcher



def create_tables():
    with app.app_context():
        db.create_all()
