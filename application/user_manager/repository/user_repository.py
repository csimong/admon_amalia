"""User repository script that contains functions to create, delete and update users in the database."""

from shared.database.database_manager import Database


class UserRepository():
    def __init__(self):
        self.db = Database()

    def add_user(self, name, surnames, email, phone):
        self.db.execute(
            "INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES (?, ?, ?, ?)", (name, surnames, email, phone))

    def get_users(self):
        return self.db.get("SELECT id, nombre, apellidos, email, telefono FROM clientes")

    def get_user_by_id(self, id):
        return self.db.get_one("SELECT id, nombre, apellidos, email, telefono FROM clientes WHERE id = ?", (id,))
    
    def update_user(self, id, name, surnames, email, phone):
        self.db.execute(
            "UPDATE clientes SET nombre = ?, apellidos = ?, email = ?, telefono = ? WHERE id = ?", (name, surnames, email, phone, id))

    def delete_user(self, id):
        self.db.execute("DELETE FROM clientes WHERE id = ?", (id,))


    def close(self):
        self.db.close()


# Create here the concatenated id of lottery table
# id = f"{numero}{sorteo}{año}"
