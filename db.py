import sqlite3

def creating_database ():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.executescript('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY,
        name TEXT
    );

    CREATE TABLE IF NOT EXISTS categories(
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );
    
    CREATE TABLE IF NOT EXISTS expenses(
        id INTEGER PRIMARY KEY,
        user_id INTEGER NOT NULL,
        category_id INTEGER NOT NULL,
        date TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(category_id) REFERENCES categories(id)
    );
    ''')
    con.commit()
    con.close()

def show_database():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
    SELECT tbl_name
    FROM sqlite_master;
    ''')
    for result in cur:
        print(result)
    con.close()

def selecting():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
    SELECT *
    FROM categories;
    ''')
    for result in cur:
        print(result)
    con.close()
def default_filling():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    categories = [(1, "Обырвалг"),
                  (2, "Алкоголь"),
                  (3, "Сладкий Бубалех"),
                  (4, "Бугульма")]
    cur.executemany('INSERT OR IGNORE INTO categories VALUES(?, ?);', categories)
    con.commit()
    con.close()

def drop_table():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.executescript('''
        DROP TABLE IF EXISTS users;
        DROP TABLE IF EXISTS expenses;
        DROP TABLE IF EXISTS categories;
        ''')
    con.commit()
    con.close()

# drop_table()
creating_database()
# show_database()
default_filling()
# selecting()
