from . import db

class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(20), unique=False)
    firstName = db.Column(db.String(20), unique=False)
    lastName = db.Column(db.String(20), unique=False)