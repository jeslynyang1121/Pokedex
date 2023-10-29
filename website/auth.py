from flask import Blueprint, render_template, request, flash
import sqlite3


auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # connect to DB
        connection = sqlite3.connect('pokemon.db')
        cursor = connection.cursor()

        # get form info
        username = request.form.get('username')
        password = request.form.get('password')

        # check if user credentials are valid
        print(request)
        query = "SELECT username, password FROM trainers WHERE username = '" + username + "' AND password = '" + password + "'"
        cursor.execute(query)
        results = cursor.fetchall()
        
        if len(results) == 1:
            # log in user
            print("Log In Successful")
            connection.close()
            return render_template("pokedex.html")
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
        connection = sqlite3.connect('pokemon.db')
        cursor = connection.cursor()

        # get form info
        username = request.form.get('username')
        password = request.form.get('password')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')

        # check if username is unique
        query = "SELECT username FROM trainers WHERE username = '" + username + "' "
        results = cursor.fetchall()
        if len(results) == 0:
            # add new user to db
            # command = "INSERT INTO trainers(username, password, firstName, lastName) VALUES (?, ?, ?, ?);"
            # info = (username, password, firstName, lastName)
            # cursor.execute(command, info)
            cursor.execute("""INSERT INTO trainers(username, password, firstName, lastName) VALUES (?, ?, ?, ?)""", (username, password, firstName, lastName))
            connection.commit()
            connection.close()
            return render_template("pokedex.html")
        else:
            # username is already taken
            print("Invalid username")
            print("username: " + username)
            print("password: " + password)
        
    return render_template("signUp.html")