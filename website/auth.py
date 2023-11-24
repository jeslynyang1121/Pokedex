from flask import Blueprint, render_template, redirect, request, url_for
from .models import User
from . import db


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form info
        username = request.form.get('username')
        password = request.form.get('password')

        # check if user credentials are valid
        results = User.query.filter_by(username = username, password = password).first()
        print(results)
        
        if results:
            # log in user
            print("Log In Successful")
            return redirect(url_for('views.pokedex'))
        else:
            # Invalid username and password
            print("Invalid username and password")
            print("username: " + username)
            print("password: " + password)
    return render_template("login.html")

@auth.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        # connect to DB 

        # get form info
        username = request.form.get('username')
        password = request.form.get('password')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        print("username: " + username + ", password: " + password)
        print("first name: " + firstName + ", last name: " + lastName)

        # check if username is unique
        results = User.query.filter_by(username=username).first()
        if results:
            # username is already taken
            print("Invalid username")
            print("username: " + username)
            print("password: " + password)
        else:
            # add new user to db
            newUser = User(username = username, password = password, firstName = firstName, lastName = lastName)
            db.session.add(newUser)
            db.session.commit()
            print("Account created")
            return redirect(url_for('views.pokedex'))
        
    return render_template("signup.html")