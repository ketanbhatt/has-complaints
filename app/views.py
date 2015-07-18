from flask import render_template, flash, redirect
from app import app
from .forms import *

@app.route('/', methods=['GET', 'POST'])
def index():
	form = ComplaintForm()
	if form.validate_on_submit():
		flash('You complained about %s' % (form.title.data))
		return redirect('/')
	return render_template('index.html',
                           title='Home',
                           form=form)


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()
	if form.validate_on_submit():
		flash('User %s signed in' % (form.email.data))
		return redirect('/')
	return render_template('signin.html',
                           title='Sign In',
                           form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if form.validate_on_submit():
		flash('You complained about %s' % (form.name.data))
		return redirect('/')
	return render_template('signup.html',
                           title='Sign Up',
                           form=form)