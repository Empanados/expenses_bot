import psycopg2

def database_connection():
    con = psycopg2.connect(
      database="expenses_bot",
      user="postgres",
      password="12345678",
      host="localhost",
      port="5433"
    )
    return con


def creating_database():
    con = database_connection()
    cur = con.cursor()
    cur.execute('''
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

creating_database()
print("Database created successfully")