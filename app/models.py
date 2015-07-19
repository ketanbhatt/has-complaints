from app import app, db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

import flask.ext.whooshalchemy as whooshalchemy

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	empId = db.Column(db.String(10), index=True, unique=True)
	is_admin = db.Column(db.Boolean, default=False)
	admin_score = db.Column(db.Float, default=0)
	_password = db.Column(db.String(128))


	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def _set_password(self, plaintext):
		self._password = bcrypt.generate_password_hash(plaintext)

	def is_correct_password(self, plaintext):
		if bcrypt.check_password_hash(self._password, plaintext):
			return True

		return False

	def is_authenticated(self):
		return True

	def is_active(self):
		return True

	def is_anonymous(self):
		return False

	def get_id(self):
		return unicode(self.id)

	def __repr__(self):
		return '<User %r>' % (self.name)

class Complaint(db.Model):
	__searchable__ = ['text']

	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(64))
	text = db.Column(db.String(400))
	timestamp = db.Column(db.DateTime)
	upvotes = db.Column(db.Integer, default=0)
	is_underProcess = db.Column(db.Boolean, default=False)
	is_resolved = db.Column(db.Boolean, default=False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	admin_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=None)

	user_rel = db.relationship("User", foreign_keys=[user_id])
	admin_rel = db.relationship("User", foreign_keys=[admin_id])

	def __repr__(self):
		return "<Complaint %r>" % (self.title)

whooshalchemy.whoosh_index(app, Complaint)