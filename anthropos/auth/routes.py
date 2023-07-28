from anthropos.auth import bp
from flask import redirect, render_template, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user
from datetime import datetime
from urllib.parse import urlsplit
from .forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm, RegistrationForm
from anthropos.models import DatabaseUser
from anthropos import db
from .reset_email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(DatabaseUser).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', category='danger')
            return redirect(url_for('auth.login'))
        elif not user.activated:
            flash('Email is not confirmed', 'warning')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        session['user_role'] = user.role
        session['login_time'] = user.last_login
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Вход в систему', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index.index'))


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
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
    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/user_confirmation/<username>/<token>')
def user_confirmation(username, token):
    user = db.session.query(DatabaseUser).filter_by(username=username).first()
    if str(user.token) == token:
        user.activated = True
        db.session.commit()
        flash('Email confirmed', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = DatabaseUser.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',
                           title='Восстановление пароля', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    user = DatabaseUser.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Восстановление пароля', form=form)