from flask import Flask, redirect, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('players.db')
    conn.row_factory  = sqlite3.Row
    return conn


def create_query(year, pos):
    if pos == "All":
            q = 'SELECT * FROM stats%s' %year
    else:
            q = 'SELECT * FROM stats%s' %year + ' WHERE "Pos" == "%s"' %pos
    return q

@app.route('/', methods=['POST','GET'])
def index():

    conn = get_db_connection()
    
    if request.method == 'POST':

        season = request.form.get('Season')
        position = request.form.get('Position')
        sql_str = create_query(season,position)
        players = conn.execute(sql_str)

        return render_template('index.html',players=players, year=season, pos=position)
    else:
        players = conn.execute('SELECT * FROM stats2022  ORDER BY "fPtsPerG" desc')
        return render_template('index.html',players=players, year="2022", pos = "All")

if __name__ == "__main__":
    app.run(debug=True)
