from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required

from app import app, db, lm, bcrypt
from .forms import *
from .models import *

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.search_form = SearchForm()

@app.route('/', methods=['GET', 'POST'])
def index():
	form = ComplaintForm()
	if form.validate_on_submit():
		complaint = Complaint(title=form.title.data, text=form.text.data, complainant=current_user)
		db.session.add(complaint)
		db.session.commit()
		flash('You complained about %s' % (form.title.data))
		return redirect(url_for('index'))

	complaints = Complaint.query.order_by('id desc').limit(20).all()
	return render_template('index.html',
                           title='Home',
                           complaints=complaints,
                           form=form)

@login_required
@app.route('/profile')
def profile():
	complaints = current_user.complaints.order_by('id desc').limit(20).all()
	return render_template('index.html',
                           title=current_user.name,
                           header=current_user.name + ": ",
                           subheader="your complaints",
                           complaints=complaints)

@app.route('/search', methods=['POST'])
def search():
	if not g.search_form.validate_on_submit():
		return redirect(url_for('index'))
	return redirect(url_for('search_results', query=g.search_form.search.data))

@app.route('/search_results/<query>')
def search_results(query):
    	results = Complaint.query.whoosh_search(query, 20).all()
    	return render_template('index.html',
    					title="Search Results",
    					header="Search Results for ",
    					subheader=query,
    					complaints=results)

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if current_user.is_authenticated():
		return redirect(url_for('index'))

	form = SigninForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first_or_404()
		if user.is_correct_password(form.password.data):
			login_user(user)
			return redirect(url_for('index'))
		else:
			return redirect(url_for('signin'))

	return render_template('signin.html',
                           title='Sign In',
                           form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		if form.password.data == form.retypePassword.data:
			user = User(name=form.name.data, email=form.email.data, empId=form.empId.data, password=form.password.data)
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('index'))

	return render_template('signup.html',
                           title='Sign Up',
                           form=form)

@login_required
@app.route('/signout')
def signout():
	logout_user()
	return redirect(url_for('index'))