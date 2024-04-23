import sqlite3


def init_db():
    conn = sqlite3.connect('Event.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXIST notes (
            date TEXT PRIMARY KEY,
            title TEXT,
            description TEXT
        )    
    ''')
    conn.commit()
    conn.close()
