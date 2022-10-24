import sqlite3

con = sqlite3.connect('db.sqlite')
cur = con.cursor()

def creating_database ():
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS directors(
        id INTEGER PRIMARY KEY,
        name TEXT,
        bithday_year INTEGER
    );

    CREATE TABLE IF NOT EXISTS movies(
        id INTEGER PRIMARY KEY,
        name TEXT,
        type TEXT,
        release_year INTEGER
    );
    ''')