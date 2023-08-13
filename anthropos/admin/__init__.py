"""
    Admin module contains all neccessary logic for admin panel
    of the Base Habilis app
"""

from anthropos.admin.models import MyAdminView, MyModelView, UserView
from anthropos.admin.admin import admin

# To better support introspection, modules should explicitly
# declare the names in their public API using the __all__ attribute.
__all__ = ['MyAdminView', 'MyModelView', 'UserView', 'admin']
