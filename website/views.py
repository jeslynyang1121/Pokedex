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

    # main query
    query = "SELECT P.id, name, image, type, height, weight, gender, post_pokemon, U.username FROM Statistics LEFT JOIN Pokemon P ON pokemon_id = P.id LEFT JOIN Evolutions E ON name = curr_pokemon LEFT JOIN User U ON user_id = U.id"

    # search for all pokemon and corresponding stats
    if request.method == 'GET':
        cursor.execute(query)
        all_pokemon_stats = cursor.fetchall()
        print(all_pokemon_stats)

        return render_template("pokedex.html", all_pokemon_stats=all_pokemon_stats)
    # sort by certain category
    elif request.method == 'POST':
        isSearch = request.form.get('search')
        isSort = request.form.get('sort')
        # search
        if isSearch is not None:
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
            query += " WHERE {} = ?"
            cursor.execute(query.format(category), [search_for])
            searched_pokemon_stats = cursor.fetchall()
            print(searched_pokemon_stats)
            connection.close()

            return render_template("pokedex.html", all_pokemon_stats=searched_pokemon_stats)

        # sort by
        elif isSort is not None:
            # get form info
            category = request.form.get('sort_category')
            if category == None or category == "number":
                print("converted")
                category = "P.id"
            print("sort by: " + category)

            query += " ORDER BY {}"
            cursor.execute(query.format(category))
            all_pokemon_stats = cursor.fetchall()
            print(all_pokemon_stats)

            return render_template("pokedex.html", all_pokemon_stats=all_pokemon_stats)
    connection.close()
    return render_template("pokedex.html")

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
        evolution = request.form.get('evolution')

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
            new_evo = Evolutions(curr_pokemon = name, post_pokemon = evolution)
            db.session.add(new_evo)
            db.session.commit()

            print("Pokemon Added Successfully")
            return redirect(url_for('views.pokedex'))
    print("Fail to add pokemon!")
    return render_template("add_pokemon.html")

@views.route('/edit_choose', methods=['GET', 'POST'])
def edit_choose():
    # connect to db
    connection = sqlite3.connect('instance/pokemon.db')
    cursor = connection.cursor()

    if request.method == 'GET':
        # query all pokemon id's
        query = "SELECT id FROM Pokemon P"
        cursor.execute(query)
        all_pokemon = cursor.fetchall()
        print(all_pokemon)
        return render_template("edit_choose.html", all_pokemon=all_pokemon)
    elif request.method == 'POST':
        # get pokemon id to edit
        id = request.form.get("id_to_edit")

        # query corresponding pokemon
        query = "SELECT P.id, name, image, type, height, weight, gender, post_pokemon, U.username FROM Statistics LEFT JOIN Pokemon P ON pokemon_id = P.id LEFT JOIN Evolutions E ON name = curr_pokemon LEFT JOIN User U ON user_id = U.id WHERE P.id = ?"
        cursor.execute(query, [id])
        pokemon_info = cursor.fetchall()
        print(pokemon_info)
        print("edit_pokemon")
        # return redirect(url_for('views.edit_pokemon', pokemon_info=pokemon_info))
        return render_template("edit_pokemon.html", pokemon_info=pokemon_info)
    
    print("fail to choose which pokemon to edit")

@views.route('/edit_pokemon', methods=['GET', 'POST'])
def edit_pokemon():
    # works similar to add_pokemon
    if request.method == 'POST':
        # find if user is editing or deleting pokemon
        isEdit = request.form.get("edit")
        isDelete = request.form.get("delete")
        print("in the post")

        if isEdit is not None:
            print("edit")
            # editing pokemon info
            # get form info
            num = request.form.get('number')
            name = request.form.get('name')
            img = request.form.get('image_link')
            type = request.form.get('type')
            height = request.form.get('height')
            weight = request.form.get('weight')
            gender = request.form.get('gender')
            evolution = request.form.get('evolution')
            trainer = request.form.get('trainer')

            # check if trainer is valid
            trainer_results = User.query.filter_by(username = trainer).first()
            print(trainer_results)
            if trainer_results:
                # get corresponding trainer id from trainer
                trainer_id = trainer_results.id
                # add pokemon to db
                new_pokemon = Pokemon.query.filter_by(id = num).first()
                new_pokemon.name = name
                db.session.commit()
                new_pokemon_stats = Statistics.query.filter_by(pokemon_id = num).first()
                new_pokemon_stats.image = img
                new_pokemon_stats.type = type
                new_pokemon_stats.height = height
                new_pokemon_stats.weight = weight
                new_pokemon_stats.gender = gender
                new_pokemon_stats.trainer = trainer
                new_pokemon_evo = Evolutions.query.filter_by(curr_pokemon = name).first()
                new_pokemon_evo.post_pokemon = evolution
                db.session.commit()

                print("Pokemon Edited Successfully")
                return redirect(url_for('views.pokedex'))
            else:
                print("Pokemon Failed to Edit Successfully")
                return redirect(url_for('views.edit_choose'))
        elif isDelete is not None:
            print("delete")
            # get form info
            num = request.form.get('number')
            name = request.form.get('name')
            print("id: " + num + ", name: " + name)

            # delete pokemon from pokedex
            old_pokemon = Pokemon.query.filter_by(id = num).first()
            old_pokemon_stats = Statistics.query.filter_by(pokemon_id = num).first()
            # old_pokemon_evo = Evolutions(curr_pokemon = name)
            print(old_pokemon)
            print(old_pokemon_stats)
            if old_pokemon is not None and old_pokemon_stats is not None:
                db.session.delete(old_pokemon)
                db.session.delete(old_pokemon_stats)
                # db.session.delete(old_pokemon_evo)
                db.session.commit()
                print("Pokemon Failed to Delete Successfully")
                return redirect(url_for('views.pokedex'))
            else:
                return redirect(url_for('views.edit_choose'))
        
    print("Fail to edit pokemon!")
    return render_template("edit_pokemon.html")
