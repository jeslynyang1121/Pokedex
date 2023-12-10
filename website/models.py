from . import db

# create models for db tables

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    username = db.Column(db.String(20), index=True)
    password = db.Column(db.String(20))
    firstName = db.Column(db.String(20))
    lastName = db.Column(db.String(20), default=None)
    statistics = db.relationship('Statistics')

class Pokemon(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(20), index=True)
    statistics = db.relationship('Statistics')
    evolutions = db.relationship('Evolutions')

class Statistics(db.Model):
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), primary_key=True, index=True)
    image = db.Column(db.String(1000), default=None)
    type = db.Column(db.Integer, default=None)
    height = db.Column(db.Integer, default=None)
    weight = db.Column(db.Integer, default=None)
    gender = db.Column(db.String(20), default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)

class Evolutions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    curr_pokemon = db.Column(db.Integer, db.ForeignKey('pokemon.name'), index=True)
    post_pokemon = db.Column(db.Integer, default=None)