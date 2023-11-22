from flask import Blueprint, render_template, redirect, request, session
from .models import User
from . import db


# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

auth = Blueprint('auth', __name__)

# db = SQLAlchemy(auth)

# class User(db.Model):
#     username = db.Column(db.String(20), primary_key=True)
#     password = db.Column(db.String(20), unique=False)
#     firstName = db.Column(db.String(20), unique=False)
#     lastName = db.Column(db.String(20), unique=False)

#     def __repr__(self):
#         return f"username : {self.username}, password: {self.password}, firstName: {self.firstName}, lastName: {self.lastName}"
 


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # connect to DB
        # connection = sqlite3.connect('pokemon.db')
        # cursor = connection.cursor()

        # get form info
        username = request.form.get('username')
        password = request.form.get('password')

        # check if user credentials are valid
        print(request)
        # query = "SELECT username, password FROM trainers WHERE username = (?) AND password = (?)"
        # cursor.execute(query, (username, password))
        # results = cursor.fetchall()
        results = User.query.filter_by(username = username, password = password).first()
        
        print(results, sep = ", ")
        
        if results:
            # log in user
            print("Log In Successful")
            # connection.close()
            return render_template("pokedex.html")
        else:
            # Invalid username and password
            print("Invalid username and password")
            print("username: " + username)
            print("password: " + password)
            return redirect("login.html")
    return render_template("login.html")

@auth.route('/signUp', methods=['GET', 'POST'])
def signUp():
    if request.method == 'POST':
        # connect to DB 
        # connection = sqlite3.connect('pokemon.db')
        # cursor = connection.cursor()

        # get form info
        username = request.form.get('username')
        password = request.form.get('password')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        print("username: " + username + ", password: " + password)
        print("first name: " + firstName + ", last name: " + lastName)

        # check if username is unique
        # query = "SELECT username FROM trainers WHERE username = (?)"
        # cursor.execute(query, username)
        # results = cursor.fetchall()
        results = User.query.filter_by(username=username).first()
        if results:
            # username is already taken
            print("Invalid username")
            print("username: " + username)
            print("password: " + password)
            return redirect("signUp.html")
        else:
            # add new user to db
            newUser = User(username = username, password = password, firstName = firstName, lastName = lastName)
            # cursor.execute("INSERT INTO trainers(username, password, firstName, lastName) VALUES (?, ?, ?, ?)", (username, password, firstName, lastName))
            db.session.add(newUser)
            db.session.commit()
            # connection.commit()
            # connection.close()
            print("Account created")
            return render_template("pokedex.html")
        
    return render_template("signUp.html")