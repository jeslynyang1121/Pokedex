from flask import Blueprint, render_template, redirect, request, url_for
from .models import User, Pokemon, Statistics, Evolutions
from . import db
import sqlite3

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/pokedex', methods=['GET', 'POST'])
def pokedex():

    # connect to db
    connection = sqlite3.connect('instance/pokemon.db')
    cursor = connection.cursor()

    # search for all pokemon and corresponding stats
    if request.method == 'GET':
        query = "SELECT P.id, name, image, type, height, weight, gender, U.username FROM Statistics LEFT JOIN Pokemon P ON pokemon_id = P.id LEFT JOIN User U ON user_id = U.id"
        cursor.execute(query)
        all_pokemon_stats = cursor.fetchall()
        print(all_pokemon_stats)

        return render_template("pokedex.html", all_pokemon_stats=all_pokemon_stats)
    # sort by certain category
    if request.method == 'POST':
        # get form info
        category = request.form.get('sort_category')
        if category == None or category == "number":
            print("converted")
            category = "P.id"
        print("sort by: " + category)

        query = "SELECT P.id, name, image, type, height, weight, gender, U.username FROM Statistics LEFT JOIN Pokemon P ON pokemon_id = P.id LEFT JOIN User U ON user_id = U.id ORDER BY {}"
        cursor.execute(query.format(category))
        all_pokemon_stats = cursor.fetchall()
        print(all_pokemon_stats)

        return render_template("pokedex.html", all_pokemon_stats=all_pokemon_stats)
    connection.commit()
    connection.close()
    return render_template("pokedex.html")

@views.route('/pokedex/search_by', methods=['GET', 'POST'])
def search_by():
    if request.method == 'POST':
        # connect to db
        connection = sqlite3.connect('instance/pokemon.db')
        cursor = connection.cursor() 

        # get form info
        category = request.form.get('search_category')
        if category == None or category == "number":
            print("converted")
            category = "P.id"
        elif category == "trainer":
            print("converted")
            category = "U.username"
        search_for = request.form.get('search_for')
        print("search by: " + category + " for " + search_for)

        # query
        query = "SELECT P.id, name, image, type, height, weight, gender, U.username FROM Statistics LEFT JOIN Pokemon P ON pokemon_id = P.id LEFT JOIN User U ON user_id = U.id WHERE {} = ?"
        cursor.execute(query.format(category), [search_for])
        searched_pokemon_stats = cursor.fetchall()
        print(searched_pokemon_stats)

        return render_template("pokedex.html", all_pokemon_stats=searched_pokemon_stats)

@views.route('/add_pokemon', methods=['GET', 'POST'])
def add_pokemon():
    if request.method == 'POST':
        # get form info
        name = request.form.get('name')
        img = request.form.get('image_link')
        type = request.form.get('type')
        height = request.form.get('height')
        weight = request.form.get('weight')
        gender = request.form.get('gender')
        trainer = request.form.get('trainer')

        # check if trainer is valid
        trainer_results = User.query.filter_by(username = trainer).first()
        print(trainer_results)
        if trainer_results:
            # get corresponding trainer id from trainer
            trainer_id = trainer_results.id
            # add pokemon to db
            new_pokemon = Pokemon(name = name)
            db.session.add(new_pokemon)
            db.session.commit()
            new_stats = Statistics(pokemon_id = new_pokemon.id, image=img, type = type, height = height, weight = weight, gender = gender, user_id = trainer_id)
            db.session.add(new_stats)
            db.session.commit()

            print("Pokemon Added Successfully")
            return redirect(url_for('views.pokedex'))
    print("Fail to add pokemon!")
    return render_template("add_pokemon.html")

@views.route('/edit_pokemon', methods=['GET', 'POST'])
def edit_pokemon():
    return render_template("pokedex.html")
