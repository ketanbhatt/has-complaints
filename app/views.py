from flask import render_template, redirect, flash, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from sqlalchemy import exc

from app import app, db, lm, bcrypt
from .forms import *
from .models import *
from datetime import datetime

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.before_request
def before_request():
	g.search_form = SearchForm()



# 
# User Management
# 

@app.route('/signin', methods=['GET', 'POST'])
def signin():
	if current_user.is_authenticated():
		return redirect(url_for('index'))

	form = SigninForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email = form.email.data).first()
		if user is None:
			flash('No user with the specified Email exists', 'warning')
			return redirect(url_for('signin'))
		elif user.is_correct_password(form.password.data):
			login_user(user)
			return redirect(url_for('index'))
		else:
			flash('Wrong password entered!', 'danger')
			return redirect(url_for('signin'))

	return render_template('signin.html',
                           title='Sign In',
                           form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		user = User(name=form.name.data, email=form.email.data, empId=form.empId.data, password=form.password.data)
		try:
			db.session.add(user)
			db.session.commit()
			login_user(user)
			return redirect(url_for('index'))
		except exc.SQLAlchemyError:
			flash('Email/Employee ID already exists', 'danger')
			return redirect(url_for('signup'))

	return render_template('signup.html',
                           title='Sign Up',
                           form=form)

@app.route('/signout')
@login_required
def signout():
	logout_user()
	return redirect(url_for('index'))



# 
# Home and Profile
# 

@app.route('/', methods=['GET', 'POST'])
def index():
	form = ComplaintForm()
	if form.validate_on_submit():
		complaint = Complaint(title=form.title.data, text=form.text.data, timestamp=datetime.now(), user_rel=current_user)
		db.session.add(complaint)
		db.session.commit()
		return redirect(url_for('index'))

	complaints = Complaint.query.order_by('id desc').limit(20).all()
	return render_template('index.html',
                           title='Home',
                           complaints=complaints,
                           form=form)

@app.route('/profile')
@login_required
def profile():
	if current_user.is_admin:
		complaints = Complaint.query.filter_by(admin_id = current_user.get_id()).order_by('id desc').limit(20).all()
		subheader = "complaints you are responsible for"
	else:
		complaints = Complaint.query.filter_by(user_id = current_user.get_id()).order_by('id desc').limit(20).all()
		subheader = "your complaints"

	return render_template('index.html',
                           title=current_user.name,
                           header=current_user.name + ": ",
                           subheader=subheader,
                           complaints=complaints)



# 
# Search
# 

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



# 
# Process Complaints
# 

@app.route('/underProcess/<int:complaint_id>')
@login_required
def set_underProcess(complaint_id):
	complaint = Complaint.query.filter_by(id = complaint_id).first()
	complaint.is_underProcess = True
	complaint.admin_rel = current_user
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/resolved/<int:complaint_id>')
@login_required
def set_resolved(complaint_id):
	complaint = Complaint.query.filter_by(id = complaint_id).first()
	complaint.is_resolved = True
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/upvote/<int:complaint_id>')
@login_required
def upvote(complaint_id):
	has_upvoted = UpvotesTable.query.filter_by(upvoter_id = current_user.get_id(), complaint_id = complaint_id).first()
	if has_upvoted is None:
		complaint = Complaint.query.filter_by(id = complaint_id).first()
		complaint.upvotes += 1
		newUpvote = UpvotesTable(upvoter_id=current_user.get_id(), complaint_id=complaint_id)
		db.session.add(newUpvote)
		db.session.commit()
		
	return redirect(url_for('index'))
	