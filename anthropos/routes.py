from flask_login import current_user, login_user, logout_user, login_required
from flask import redirect, url_for, flash, render_template, jsonify, request
from anthropos.models import DatabaseUser, ArchaeologicalSite, Researcher, Region, FederalDistrict
from anthropos import app, db, mail
from flask_mail import Message
from anthropos.forms import RegistrationForm, LoginForm, ResearcherForm, ArchaeologicalSiteForm, EditProfileForm, ResetPasswordRequestForm, ResetPasswordForm
from datetime import datetime
from urllib.parse import urlsplit
from anthropos.lib.reset_email import send_password_reset_email


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
            flash('Invalid username or password', category='danger')
            return redirect(url_for('login'))
        elif not user.activated:
            flash('Email is not confirmed', 'warning')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        user.last_login = datetime.utcnow()
        db.session.commit()
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
        user.save_to_db(db.session)
        user.send_confirmation_email()
        flash(f'Congratulations, {user.username} is now a registered user!', 'success')
        flash(f'Please confirm your account - check your mail', 'info')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user_confirmation/<username>/<token>')
def user_confirmation(username, token):
    user = db.session.query(DatabaseUser).filter_by(username=username).first()
    if str(user.token) == token:
        user.activated = True
        db.session.commit()
        flash('Email confirmed', 'success')
    return redirect(url_for('login'))


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.session.query(DatabaseUser).filter_by(username=username).first_or_404()
    sites = db.session.query(ArchaeologicalSite).filter_by(creator_id=user.id).all()
    return render_template('profile.html', user=user, sites=sites)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.middle_name = form.middle_name.data
        current_user.affiliation = form.affiliation.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your changes have been saved.', 'success')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.middle_name.data = current_user.middle_name
        form.affiliation.data = current_user.affiliation
        form.email.data = current_user.email
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@app.route('/submit_researcher', methods=['GET', 'POST'])
@login_required
def submit_researcher():
    form = ResearcherForm()
    if form.validate_on_submit():
        researcher = Researcher(form.first_name.data,
                                form.last_name.data,
                                form.middle_name.data)
        db.session.add(researcher)
        db.session.commit()
        return redirect(url_for('submit_researcher'))
    return render_template('submit_researcher.html', title='Submit researcher form', form=form)


@app.route('/submit_site', methods=['GET', 'POST'])
@login_required
def submit_site():
    researchers = sorted([(0, 'Выберите исследователя')] + \
                  [(researcher.id, researcher.__str__()) for researcher in Researcher.get_all(db.session)])
    fed_districts = sorted([(0, 'Выберите федеральный округ')] + \
                    [(district.id, district.name) for district in FederalDistrict.get_all(db.session)])
    site_form = ArchaeologicalSiteForm(researchers, fed_districts)
    if site_form.validate_on_submit():
        site = ArchaeologicalSite(site_form.name.data,
                                  site_form.long.data,
                                  site_form.lat.data,
                                  current_user,
                                  db.session.query(Researcher).filter_by(id=site_form.researcher.data).first(),
                                  db.session.query(Region).filter_by(id=site_form.region.data).first()
                                  )
        db.session.add(site)
        db.session.commit()
        return redirect(url_for('submit_site'))
    return render_template('site_input.html', title='Submit site form', form=site_form)


@app.route('/submit_site/<fd_id>')
def region(fd_id):
    regions = Region.query.filter_by(federal_districts_id=fd_id).all()
    regionArray = [{'id': 0, 'name': 'Выберите субъект'}]
    for region in regions:
        regionObj = {}
        regionObj['id'] = region.id
        regionObj['name'] = region.name
        regionArray.append(regionObj)
    return jsonify({'regions': regionArray})


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = DatabaseUser.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = DatabaseUser.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash('Your password has been reset.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)
