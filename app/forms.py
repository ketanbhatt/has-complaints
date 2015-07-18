from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class ComplaintForm(Form):
	title = TextField('Complaint Title', validators=[DataRequired()])
	text = TextAreaField('Complain Text', validators=[DataRequired()])

class SigninForm(Form):
	email = StringField('email', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember_me = BooleanField('Remember me', default=False)

class SignupForm(Form):
	name = TextField('Username', validators=[DataRequired()]) 
	email = StringField('Email', validators=[DataRequired()])
	empId = StringField('Employee ID', validators=[DataRequired()])
	password = PasswordField('Password', validators=[DataRequired()])
	retypePassword = PasswordField('Retype Password', validators=[DataRequired()])