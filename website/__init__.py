from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.secret_key = "password"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///pokemon.db'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')

    from .models import User, Pokemon, Statistics, Evolutions
    
    with app.app_context():
        db.create_all()

    return app