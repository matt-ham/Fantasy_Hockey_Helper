import sqlite3

## init database

conn = sqlite3.connect('players.db')

c = conn.cursor()

conn.commit()

