"""Database connection and management file. It contains functions to connect to the database."""
import sqlite3
from config import DB_NAME
class Database():
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        # Activate foreign keys for the connection
        self.conn.execute("PRAGMA foreign_keys = ON")
        
    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        
    def get(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def close(self):
        self.conn.close()

if "__name__" == "__main__":
    db = Database()
    with open("database/schema.sql", "r") as f:
        db.cursor.executescript(f.read())
        db.conn.commit()
    db.close()