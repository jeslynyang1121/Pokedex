import sqlite3

connection = sqlite3.connect("pokemon.db")
cursor = connection.cursor()

# create tables in DB
createTrainers = "CREATE TABLE IF NOT EXISTS trainers (username TEXT PRIMARY KEY, password TEXT, firstName TEXT, lastName TEXT)"
createPokemon = "CREATE TABLE IF NOT EXISTS pokemon (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"
createStatistics = "CREATE TABLE IF NOT EXISTS statistics (id INTEGER PRIMARY KEY, type TEXT, height INTEGER, weight INTEGER, gender TEXT, trainer_id INTEGER, evolution_id INTEGER)"
createEvolutions = "CREATE TABLE IF NOT EXISTS evolutions (id INTEGER PRIMARY KEY AUTOINCREMENT, pre_pokemon_id INTEGER, curr_pokemon_id INTEGER)"
cursor.execute(createTrainers)
cursor.execute(createPokemon)
cursor.execute(createStatistics)
cursor.execute(createEvolutions)

connection.commit()
connection.close()