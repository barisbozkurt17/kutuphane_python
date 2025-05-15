import sqlite3 as lit
import os

def create_table_if_not_exists(cur, name, query):
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{name}'")
    if cur.fetchone():
        print(f"Warning: Table '{name}' already exists!")
    else:
        cur.execute(query)
        print(f"Table '{name}' created successfully")

def create_database_and_tables(db_name='db.db'):
    db_exists = os.path.exists(db_name)

    try:
        db = lit.connect(db_name)
        cur = db.cursor()

        if not db_exists:
            print(f"Database '{db_name}' created.")
        else:
            print(f"Database '{db_name}' already exists.")

        # Tablo oluşturma sorguları
        tables = {
            "kullanicilar": """
                CREATE TABLE kullanicilar (
                    id INTEGER PRIMARY KEY, 
                    name TEXT, 
                    email TEXT
                )
            """,
            "users": """
                CREATE TABLE users (
                    tcno INTEGER,
                    adsoyad TEXT,
                    telefon TEXT,
                    mevcut INTEGER DEFAULT 0,
                    okunan INTEGER DEFAULT 0
                )
            """,
            "books": """
                CREATE TABLE books (
                    id INTEGER PRIMARY KEY,
                    barcode TEXT,
                    title TEXT NOT NULL,
                    author TEXT,
                    publisher TEXT,
                    year INTEGER,
                    count INTEGER DEFAULT 1,
                    read_count INTEGER DEFAULT 0
                )
            """,
            "loans": """
                CREATE TABLE loans (
                    id INTEGER PRIMARY KEY,
                    tcno INTEGER,
                    barcode TEXT,
                    borrow_date TEXT,
                    return_date TEXT
                )
            """
        }

        for table_name, query in tables.items():
            create_table_if_not_exists(cur, table_name, query)

        db.commit()

    except lit.Error as e:
        print(f"Error: {e}")

    finally:
        db.close()

