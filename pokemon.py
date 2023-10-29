import sqlite3

connection = sqlite3.connect("grocery.db")
cursor = connection.cursor()

command = "CREATE TABLE IF NOT EXISTS trainers(id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, username TEXT, password TEXT)"
cursor.execute(command)

connection.commit()
connection.close()