"""
    Models of flask_admin package are customized
    ro restrict access for all users without 'admin' role.
    Basic customization added to Users view:
    excluded columns with password hash, editing in modals etc.
"""
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
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('index.index'))


class UserView(ViewAccessControl, ModelView):
    """
    UserView inherits from flask_admin base model and
    ViewMixin, where the neccessary logic for granting
    access to the admin panel is implemented.
    Model contains basic view customization for
    users management page.

    Args:
        ViewAccessControl (anthropos.admin.models.ViewAccessControl):
        Model with overwritten access methods
        ModelView (flask_admin.contrib.sqla.ModelView):
        Base flask_admin view model
    """
    to_exclude: list[str] = ['password_hash', 'token', 'last_login', 'created', 'email']
    can_view_details: bool = True
    column_exclude_list: list[str] = to_exclude
    create_modal: bool = True
    edit_modal: bool = True
    form_excluded_columns: list[str] = to_exclude
    form_choicesd: dict[str, list[str]] = {'role': [('user', 'user'), ('admin', 'admin')]}


class MyModelView(ViewAccessControl, ModelView):
    """
    MyModelView inherits from flask_admin base model
    and custom view mixin, which restricts the access to view for
    all non-'admin' users.

    Args:
        ViewAccessControl (anthropos.admin.models.ViewAccessControl):
        Model with overwritten access methods
        ModelView (flask_admin.contrib.sqla.ModelView):
        Base flask_admin view model
    """
    pass


class MyAdminView(ViewAccessControl, AdminIndexView):
    """
    MyAdminView inherits from flask_admin admin index view
    and custom view mixin, which restricts the access to view for
    all non-'admin' users.

    Args:
        ViewAccessControl (anthropos.admin.models.ViewAccessControl):
        Model with overwritten access methods
        AdminIndexView (flask_admin.AdminIndexView):
        Base flask_admin index view model
    """
    pass
