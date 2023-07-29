from anthropos.auth import bp
from flask import redirect, render_template, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user
from datetime import datetime
from urllib.parse import urlsplit
from anthropos.auth.forms import LoginForm, ResetPasswordRequestForm, ResetPasswordForm, RegistrationForm
from anthropos.models import DatabaseUser
from anthropos import db
from anthropos.auth.reset_email import send_password_reset_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = DatabaseUser.get_one_by_attr(DatabaseUser.username,
                                            form.username.data,
                                            db.session)
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        session['user_role'] = user.role
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
        flash(f'Поздравляем, {user.username}, Вы зарегистрированы!', 'success')
        flash(f'Пожалуйста, подвертдите Ваш адрес почты - пройдите по ссылке в письме', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Регистрация', form=form)


@bp.route('/user_confirmation/<username>/<token>')
def user_confirmation(username, token):
    user = DatabaseUser.get_one_by_attr(DatabaseUser.username,
                                        username,
                                        db.session)
    if str(user.token) == token:
        user.activated = True
        db.session.commit()
        flash('Email подтвержден', 'success')
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = DatabaseUser.get_one_by_attr(DatabaseUser.email,
                                        form.email.data,
                                        db.session)
        send_password_reset_email(user)
        flash('Проверьте свой почтовый ящик для дальнейших инструкций', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',
                           title='Восстановление пароля', form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        # return redirect(url_for('index.index'))
        logout_user()
    user = DatabaseUser.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль изменен.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', title='Восстановление пароля', form=form)