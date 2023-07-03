from flask import redirect, render_template, flash, url_for
from anthropos.register import bp
from flask_login import current_user
from .forms import RegistrationForm
from anthropos.models import DatabaseUser
from anthropos import db
from datetime import datetime


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = DatabaseUser(form.username.data,
                            form.password.data,
                            form.first_name.data,
                            form.last_name.data,
                            form.affiliation.data,
                            form.email.data,
                            datetime.utcnow(),
                            datetime.utcnow(),
                            form.middle_name.data
                            )
        user.save_to_db(db.session)
        user.send_confirmation_email()
        flash(f'Congratulations, {user.username} is now a registered user!', 'success')
        flash(f'Please confirm your account - check your mail', 'info')
        return redirect(url_for('auth.login'))
    return render_template('register.html', title='Register', form=form)


@bp.route('/user_confirmation/<username>/<token>')
def user_confirmation(username, token):
    user = db.session.query(DatabaseUser).filter_by(username=username).first()
    if str(user.token) == token:
        user.activated = True
        db.session.commit()
        flash('Email confirmed', 'success')
    return redirect(url_for('auth.login'))