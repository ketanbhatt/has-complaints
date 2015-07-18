from app import db, bcrypt
from sqlalchemy.ext.hybrid import hybrid_property

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(64), index=True)
	email = db.Column(db.String(120), index=True, unique=True)
	empId = db.Column(db.String(10), index=True, unique=True)
	_password = db.Column(db.String(128))
	complaints = db.relationship('Complaint', backref="complainant", lazy="dynamic")

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
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(64))
	text = db.Column(db.String(400))
	timestamp = db.Column(db.DateTime)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return "<Complaint %r>" % (self.title)