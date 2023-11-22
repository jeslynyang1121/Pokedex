import sqlite3

connection = sqlite3.connect("pokemon.db")
cursor = connection.cursor()

# create tables in DB
createTrainers = "CREATE TABLE IF NOT EXISTS trainers (username TEXT PRIMARY KEY, password TEXT, firstName TEXT, lastName TEXT)"
createTrainersIndex = "CREATE INDEX idx_loginCheck ON trainers (username, password)"

createPokemon = "CREATE TABLE IF NOT EXISTS pokemon (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)"
createPokemonIndex1 = "CREATE INDEX idx_pkmID ON pokemon (id)"
createPokemonIndex2 = "CREATE INDEX idx_pkmName ON pokemon (name)"

createStatistics = "CREATE TABLE IF NOT EXISTS statistics (id INTEGER PRIMARY KEY, type TEXT, height INTEGER, weight INTEGER, gender TEXT, trainer_id INTEGER, evolution_id INTEGER)"

createEvolutions = "CREATE TABLE IF NOT EXISTS evolutions (id INTEGER PRIMARY KEY AUTOINCREMENT, pre_pokemon_id INTEGER, curr_pokemon_id INTEGER)"

# create all tables and indeces
cursor.execute(createTrainers)
cursor.execute(createTrainersIndex)
cursor.execute(createPokemon)
cursor.execute(createPokemonIndex1)
cursor.execute(createPokemonIndex2)
cursor.execute(createStatistics)
cursor.execute(createEvolutions)

connection.commit()
connection.close()