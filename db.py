import sqlite3
import datetime

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
    expenses = [(357655661, 1, 100, '01.01.2022'),
                (357655661, 2, 200, '02.01.2022')]
    cur.executemany('INSERT OR IGNORE INTO categories VALUES(?, ?);', categories)
    cur.execute('''INSERT OR IGNORE INTO users VALUES(?, ?);''', [357655661, 'Empanadosito'])
    cur.executemany('INSERT OR IGNORE INTO expenses (user_id, category_id, expense, date) VALUES(?, ?, ?, ?);', expenses)
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
        SELECT SUM(expenses.expense)
        FROM users
        JOIN expenses ON users.id = expenses.user_id
        GROUP BY users.id
        HAVING users.id = ?;
        ''', (user_id, ))
    for result in cur:
        return result[0]
    con.close()

def save_new_user(id, name):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''INSERT OR IGNORE INTO users VALUES(?, ?);''', [id, name])
    con.commit()
    con.close()

def new_expese(value, category, user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
        SELECT *
        FROM categories;
        ''')
    categories = set()
    for result in cur:
        categories.add(result)
    for i in categories:
        if i[1] == category:
            category_id = i[0]
    current_date = str(datetime.datetime.now())
    print(user_id, category_id, value, current_date)
    cur.executemany('''INSERT OR IGNORE INTO expenses (user_id, category_id, expense, date) 
        VALUES(?, ?, ?, ?);''', [(user_id, category_id, value, current_date)])
    con.commit()
    con.close()


def clear_expenses(user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
            DELETE FROM expenses
            WHERE user_id = ?;
            ''', [user_id])
    con.commit()
    con.close()


def user_expenses_list(user_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    cur.execute('''
            SELECT expenses.expense, categories.name
            FROM expenses
            JOIN categories ON categories.id = expenses.category_id
            WHERE expenses.user_id = ?;
            ''', (user_id,))
    list = []
    for result in cur:
        list.append(result)
    return list
    con.close()


drop_table()
creating_database()
# show_database()
default_filling()