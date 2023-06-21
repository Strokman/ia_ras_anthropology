from flask_login import current_user, login_user, logout_user, login_required
from flask import redirect, url_for, flash, render_template, jsonify
from anthropos.models import DatabaseUser, ArchaeologicalSite, Epoch, Sex, Researcher, Individ, Grave, Region
from anthropos import app, db
from anthropos.forms import RegistrationForm, LoginForm, ResearcherForm, ArchaeologicalSiteForm
from datetime import datetime
from urllib.parse import unquote


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
        db.session.add(user)
        db.session.commit()
        flash(f'Congratulations, {user.username} is now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = db.session.query(DatabaseUser).filter_by(username=username).first_or_404()
    sites = db.session.query(ArchaeologicalSite).filter_by(creator_id=user.id).all()
    return render_template('user.html', user=user, sites=sites)


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
    researchers = [(researcher.id, researcher.__str__()) for researcher in Researcher.get_all()]
    regions = Region.get_all()
    site_form = ArchaeologicalSiteForm(researchers, regions)
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
    return render_template('site_input.html', title='Submit site form', site_form=site_form)


@app.route('/submit_site/<fd_id>')
def city(fd_id):

    regions = Region.query.filter_by(federal_districts_id=fd_id).all()

    regionArray = []

    for region in regions:
        regionObj = {}
        regionObj['id'] = region.id
        regionObj['name'] = region.name
        regionArray.append(regionObj)

    return jsonify({'regions' : regionArray})
