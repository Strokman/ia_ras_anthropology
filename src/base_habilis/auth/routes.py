"""
    Module contains all routes of auth package
"""
import datetime
from urllib.parse import urlsplit

from flask import (
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for
    )
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
    )
from werkzeug.wrappers import Response

from src.repository import session
from src.base_habilis.auth import bp
from src.base_habilis.auth.forms import (
    LoginForm,
    ResetPasswordRequestForm,
    ResetPasswordForm,
    RegistrationForm
    )
from src.repository.models import User, admin_required


@bp.route('/login', methods=['GET', 'POST'])
def login() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user: User | None = User.get_one_by_attr('username', session, form.username.data)
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.datetime.now(datetime.UTC),
        session.commit()
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Вход в систему', form=form)


@bp.route('/logout')
def logout() -> Response:
    logout_user()
    return redirect(url_for('index.index'))


@bp.route('/register', methods=['GET', 'POST'])
@admin_required
@login_required
def register() -> Response | str:
    # if current_user.is_authenticated:
    #     return redirect(url_for('index.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(form.username.data,
                            form.password.data,
                            form.first_name.data,
                            form.last_name.data,
                            form.affiliation.data,
                            form.email.data,
                            datetime.datetime.now(datetime.UTC),
                            datetime.datetime.now(datetime.UTC),
                            form.middle_name.data
                            )
        if user.email == 'anton.strokov@me.com':
            user.role = 'admin'
        user.save()
        user.send_confirmation_email()

        current_app.logger.info(f'User created - {user.username} - {user}')

        flash(f'Поздравляем, {user.username}, Вы зарегистрированы!', 'success')
        flash('Пожалуйста, подвертдите Ваш адрес почты - пройдите по ссылке в письме', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/user_confirmation/<username>/<token>')
def user_confirmation(username, token) -> Response:
    user: User | None = User.get_one_by_attr('username', session, username)
    if str(user.token) == token:
        user.activated = True
        session.commit()
        flash('Email подтвержден', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request() -> Response | str:
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.get_one_by_attr('email', session,
                                            form.email.data
                                            )
        user.send_password_reset_email()
        flash('Проверьте свой почтовый ящик для дальнейших инструкций', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',
                           title='Восстановление пароля', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token) -> Response | str:
    if current_user.is_authenticated:
        logout_user()
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        session.commit()
        flash('Ваш пароль изменен.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Восстановление пароля', form=form)
