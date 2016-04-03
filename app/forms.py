from flask.ext.wtf import Form
from wtforms import TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo

class ComplaintForm(Form):
	title = StringField('Complaint Title', validators=[DataRequired()])
	text = TextAreaField('Complain Text', validators=[DataRequired(), Length(max=300)])

class SigninForm(Form):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])

class SignupForm(Form):
	name = StringField('Username', validators=[DataRequired(), Length(max=20)]) 
	email = StringField('Email', validators=[DataRequired()])
	empId = StringField('Employee ID', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired(), Length(min=6), EqualTo('retypePassword', message='Passwords must match')])
	retypePassword = PasswordField('Retype Password', validators=[DataRequired()])

class SearchForm(Form):
	search = StringField('search', validators=[DataRequired()])