import sqlite3

db_name = "library.db"

def connect_db():
    conn = sqlite3.connect(db_name)
    return conn

def initialize_db():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
                   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   username TEXT NOT NULL UNIQUE,
                   email TEXT NOT NULL UNIQUE,
                   password TEXT NOT NULL, 
                   is_admin INTEGER DEFAULT 0
                   );
                   """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Books (
                   book_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   author TEXT NOT NULL,
                   isbn TEXT NOT NULL, 
                   copies INTEGER DEFAULT 1
                   );
                   """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Checkouts (
                   cust_id INTEGER PRIMARY KEY AUTOINCREMENT,
                   user_id INTEGER NOT NULL,
                   book_id INTEGER NOT NULL,
                   checkout_date DATE DEFAULT CURRENT_DATE, 
                   return_date DATE,
                   fine REAL DEFAULT 0,
                   FOREIGN KEY(user_id) REFERENCES Users(user_id),
                   FOREIGN KEY(book_id) REFERENCES Books(book_id)
                   );
                   """)
    

    conn.commit()
    conn.close()

def execute_query(query, parameters = ()):
    try:
        print(f"Executing Query: {query} with Parameters: {parameters}")
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(query, parameters)
        conn.commit()
        conn.close()
    except sqlite3.IntegrityError as e:
        print(f"Database Integrity Error: {e}")  # Handle unique constraints for username and email
        raise
    except Exception as e:
        print(f"Database Error: {e}")
        raise
    

def fetch_query(query, parameters = ()):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(query, parameters)
    results = cursor.fetchall()
    conn.close()
    return results

initialize_db()
