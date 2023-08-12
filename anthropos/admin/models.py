from flask import redirect, url_for, flash
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.wrappers import Response


class ViewAccessControl:
    """
    ViewAccessControl
    Class is intended to override default
    is_accessible() and inaccessible_callback()
    methods as prescribed in flask_admin docs.
    It restricts access for all users who doesn't have
    'admin' role
    """

    def is_accessible(self) -> True | False:
        """
        is_accessible() method validates if the current_user
        has 'admin' role

        Returns:
            True | False: Result of validation
        """
        if not current_user.is_anonymous:
            return current_user.is_admin()
        return False

    def inaccessible_callback(self, name, **kwargs) -> Response:
        """
        inaccessible_callback If user doesn't have enough rights
        to access the admin panel he will be redirected to index page

        Args:
            name (_type_): _description_

        Returns:
            Response: Redirects user to the index page
        """
        print('kek')
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('index.index'))


class UserView(ViewAccessControl, ModelView):
    """
    UserView inherits from flask_admin base model and
    ViewMixin, where the neccessary logic for granting
    access to the admin panel is implemented.
    
    Args:
        ModelView (from flask_admin.contrib.sqla.ModelView):
        Base flask_admin view Model
        ViewMixin (anthropos.admin.models.ViewMixin):
        Model with overwritten access methods
    """
    to_exclude = ['password_hash', 'token', 'last_login', 'created', 'email']
    can_view_details = True
    column_exclude_list = to_exclude
    create_modal = True
    edit_modal = True
    form_excluded_columns = to_exclude
    form_choices = {'role': [('user', 'user'), ('admin', 'admin')]}


class MyModelView(ViewAccessControl, ModelView):
    pass


class MyAdminView(ViewAccessControl, AdminIndexView):
    pass
