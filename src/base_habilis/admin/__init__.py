"""
    Admin package contains all neccessary logic for admin panel
    of the Base Habilis app
"""

from src.base_habilis.admin.models import MyAdminView, MyModelView, UserView
from src.base_habilis.admin.admin import admin

# To better support introspection, modules should explicitly
# declare the names in their public API using the __all__ attribute.
__all__ = ['MyAdminView', 'MyModelView', 'UserView', 'admin']
