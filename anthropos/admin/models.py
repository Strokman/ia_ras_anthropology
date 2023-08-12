from flask import redirect, url_for, flash
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class ViewAccessControl:

    def is_accessible(self):
        if not current_user.is_anonymous:
            return current_user.is_admin()
        return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        flash('Недостаточно прав', 'warning')
        return redirect(url_for('index.index'))


class UserView(ViewAccessControl, ModelView):
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
