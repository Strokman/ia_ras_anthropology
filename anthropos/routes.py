from flask_login import current_user, login_user, logout_user, login_required
from flask import redirect, url_for, flash, render_template
from anthropos.models import DatabaseUser, ArchaeologicalSite, Epoch, Sex, Researcher, Individ, Grave
from anthropos import app, db
from anthropos.forms import RegistrationForm, LoginForm

from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Index')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(DatabaseUser).filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
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
        db.session.add(user)
        db.session.commit()
        flash(f'Congratulations, {user.username} is now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
