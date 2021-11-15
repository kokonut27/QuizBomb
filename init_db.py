import sqlite3 
import os

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
  connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (username, password) VALUES (?, ?)", (os.environ["USER"], os.environ["PASSWORD"]))

connection.commit()
connection.close()