import sqlite3
from os.path import exists

class Favorites:
    
    def __init__(self, filename):
        self.filename = filename
        if not exists(filename):
            with sqlite3.connect(filename) as db:
                cursor = db.cursor()
                cursor.execute("""CREATE TABLE favorites(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        uid VARCHAR,
                        tid VARCHAR,
                        ip VARCHAR,
                        port VARCHAR,
                        key VARCHAR
                    )""")
    
    def add(self, uid, tid, ip, port, key):
        with sqlite3.connect(self.filename) as db:
            cursor = db.cursor()
            cursor.execute('INSERT INTO favorites(uid, tid, ip, port, key) VALUES(?, ?, ?, ?, ?)', (uid, tid, ip, port, key))
    
    def get(self):
        with sqlite3.connect(self.filename) as db:
            cursor = db.cursor()
            cursor.execute('SELECT * FROM favorites')
            data = cursor.fetchall()
        return data

    def remove(self, id):
        with sqlite3.connect(self.filename) as db:
            cursor = db.cursor()
            cursor.execute('DELETE FROM favorites WHERE id=?', id)

    def clear(self):
        with sqlite3.connect(self.filename) as db:
            cursor = db.cursor()
            cursor.execute('DELETE FROM favorites')