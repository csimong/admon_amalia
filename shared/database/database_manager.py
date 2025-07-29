"""Database connection and management file. It contains functions to connect to the database."""
import sqlite3
from shared.config import DB_NAME

class Database():
    def __init__(self, db_name=DB_NAME):
        if db_name is None:
            raise Exception("Database name cannot be None. Check .env file.")
        self.database_location = 'shared/database/'
        self.conn = sqlite3.connect(self.database_location + db_name)
        self.cursor = self.conn.cursor()
        
        # Activate foreign keys for the connection
        self.conn.execute("PRAGMA foreign_keys = ON")
        
    def init_database(self):
        with open(self.database_location + "schema.sql", "r") as f:
            self.cursor.executescript(f.read())
            self.conn.commit()
        self.close()
        
    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()
        
    def get(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def get_one(self, query, params=()):
        self.cursor.execute(query, params)
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()
