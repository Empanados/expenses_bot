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
        expense INTEGER NOT NULL,
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

def selecting_categories():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
    SELECT *
    FROM categories;
    ''')
    categories = set()
    for result in cur:
        categories.add(result[1])
    con.close()
    return categories



def default_filling():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    categories = [(1, "Обырвалг"),
                  (2, "Алкоголь"),
                  (3, "Сладкий Бубалех"),
                  (4, "Бугульма")]
    expenses = [(1, 1, 1, 100, '01.01.2022'),
                (2, 1, 1, 200, '02.01.2022')]
    cur.executemany('INSERT OR IGNORE INTO categories VALUES(?, ?);', categories)
    # cur.execute('''INSERT OR IGNORE INTO users VALUES(?, ?);''', [1, 'Арнольд'])
    # cur.executemany('INSERT OR IGNORE INTO expenses VALUES(?, ?, ?, ?, ?);', expenses)
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

def balance(user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
        SELECT users.name, SUM(expenses.expense)
        FROM users
        JOIN expenses ON users.id = expenses.user_id
        GROUP BY users.id
        HAVING users.id = ?;
        ''', user_id)
    for result in cur:
        print(result[1])
    con.close()

def save_new_user(id, name):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''INSERT OR IGNORE INTO users VALUES(?, ?);''', [id, name])
    con.commit()
    con.close()



drop_table()
creating_database()
# show_database()
default_filling()
# balance('1')
