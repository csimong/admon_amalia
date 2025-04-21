"""User management file. It contains functions to create, delete and update users."""

from database.database import Database


class UserManager():
    def __init__(self):
        self.db = Database()

    def add_user(self, name, surnames, email, phone):
        self.db.execute(
            "INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES (?, ?, ?, ?)", (name, surnames, email, phone))

    def get_users(self):
        return self.db.get("SELECT id, nombre, apellidos, email, telefono FROM clientes")

    def close(self):
        self.db.close()


# Create here the concatenated id of lottery table
# id = f"{numero}{sorteo}{año}"
