from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view =  "signin"
bcrypt = Bcrypt(app)

def calc_hotness(timestamp, upvotes):
	age_in_hours = (datetime.now() - timestamp).total_seconds()//3600
	return upvotes*5 // pow((age_in_hours+2),1.8)

from app import views, models