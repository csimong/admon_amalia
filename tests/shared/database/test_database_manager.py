"""Tests for the database manager script."""

import pytest
from shared.database.database_manager import Database
import sqlite3

# UNIT TESTS
@pytest.fixture
def in_memory_database():
    """
    Create an instance of the Database class in memory for testing.
    """

    db = Database(":memory:")
    yield db
    db.close()


def test_database_raises_exception_if_name_is_none():
    """
    Tests that the Database class raises an exception if the database name is None.
    """
    with pytest.raises(Exception, match="Database name cannot be None"):
        Database(db_name=None)


def test_pragma_foreign_keys_are_activated(in_memory_database):
    """
    Tests that PRAGMA foreign_keys is activated in the database.
    """
    db = in_memory_database
    result = db.get("PRAGMA foreign_keys")
    assert result[0][0] == 1


def test_execute_and_get_functions(in_memory_database):
    """
    Tests that the execute and get functions work as expected.
    """
    db = in_memory_database
    db.execute("CREATE TABLE clientes \
        (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, \
        apellidos TEXT NOT NULL, email TEXT, telefono TEXT)")
    db.execute("INSERT INTO clientes \
        (nombre, apellidos, email, telefono) \
        VALUES (?, ?, ?, ?)",
               ("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234"))

    result = db.get(
        "SELECT id, nombre, apellidos, email, telefono FROM clientes")

    assert len(result) == 1
    assert result[0] == (1, "David", "Bisbal",
                         "davidbisbal@gmail.com", "+34671345234")


def test_get_one_function(in_memory_database):
    """
    Tests that the get_one function works as expected.
    """
    db = in_memory_database
    db.execute("CREATE TABLE clientes \
        (id INTEGER PRIMARY KEY AUTOINCREMENT, nombre TEXT NOT NULL, \
        apellidos TEXT NOT NULL, email TEXT, telefono TEXT)")
    db.execute("INSERT INTO clientes \
        (nombre, apellidos, email, telefono) \
        VALUES (?, ?, ?, ?)",
               ("Tomatito", "Fernández", "tomatitofernandez@gmail.com", "+34671345237"))

    result = db.get_one(
        "SELECT id, nombre, apellidos, email, telefono FROM clientes WHERE id = ?",
        (1,))

    assert result == (1, "Tomatito", "Fernández",
                      "tomatitofernandez@gmail.com", "+34671345237")


def test_close_closes_connection(in_memory_database):
    """
    Tests that the close function closes the connection to the database.
    """
    db = in_memory_database
    db.close()

    with pytest.raises(sqlite3.ProgrammingError):
        db.execute("CREATE TABLE test (id INTEGER)")


# INTEGRATION TESTS
@pytest.fixture
def initializated_database():
    """
    Create an instance of the Database class in memory for testing and initialize 
    it using schema.sql.
    """
    db = Database(":memory:")
    db.init_database()
    yield db
    db.close()


def test_database_initialization_creates_tables(initializated_database):
    """
    Tests that tables specified in schema.sql are created .
    """
    db = initializated_database
    tables = db.get("SELECT name FROM sqlite_master WHERE type='table'")
    table_names = [table[0] for table in tables]
    assert {"clientes", "loteria",
            "reservas_loteria_cliente"}.issubset(table_names)


def test_insert_and_get_cliente(initializated_database):
    """
    Tests that a new cliente can be inserted and retrieved from the database.
    """
    db = initializated_database
    db.execute("INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES \
               (?, ?, ?, ?)", ("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234"))
    
    cliente = db.get_one("SELECT nombre, apellidos from clientes WHERE id = 1")
    assert cliente == ("David", "Bisbal")

def test_insert_null_cliente(initializated_database):
    """
    Tests that a null cliente cannot be inserted into the database.
    """
    db = initializated_database
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES \
               (?, ?, ?, ?)", (None, None, "davidbisbal@gmail.com", "+34671345234"))

def test_insert_and_get_loteria(initializated_database):
    """
    Tests that a new loteria can be inserted and retrieved from the database.
    """
    db = initializated_database 
    db.execute("INSERT INTO loteria (numero, sorteo, año, precio) VALUES \
               (?, ?, ?, ?)", (10797, 1, 2025, 3))
    loteria = db.get_one("SELECT numero, sorteo, año, precio from loteria WHERE id = 1")
    assert loteria == (10797, 1, 2025, 3)
    
def test_insert_null_loteria(initializated_database):
    """
    Tests that a null loteria record cannot be inserted into the database.
    """
    db = initializated_database
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO loteria (numero, sorteo, año, precio) VALUES \
               (?, ?, ?, ?)", (None, None, None, None))

def test_insert_and_get_reservas_loteria_cliente(initializated_database):
    """
    Tests that a new reservas_loteria_cliente record can be inserted and 
    retrieved from the database.
    """
    db = initializated_database
    db.execute("INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES \
               (?, ?, ?, ?)", ("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234"))
    id_cliente = db.get_one("SELECT id from clientes WHERE nombre = 'David'")[0]
    
    db.execute("INSERT INTO loteria (numero, sorteo, año, precio) VALUES \
               (?, ?, ?, ?)", (10797, 1, 2025, 3))
    id_loteria = db.get_one("SELECT id from loteria WHERE numero = 10797")[0]
    
    db.execute("INSERT INTO reservas_loteria_cliente (id_cliente, id_loteria, cantidad_decimos) VALUES \
               (?, ?, ?)", (id_cliente, id_loteria, 1),)
    
    reserva = db.get_one("SELECT id_cliente, id_loteria, cantidad_decimos from reservas_loteria_cliente \
        WHERE id = 1")
    assert reserva == (1, 1, 1)
    
def test_check_constraint_in_reservas_loteria_cliente(initializated_database):
    """
    Tests that cantidad de decimos en reservas_loteria_cliente es mayor que 0.
    """
    db = initializated_database
    db.execute("INSERT INTO clientes (nombre, apellidos, email, telefono) VALUES \
               (?, ?, ?, ?)", ("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234"))
    id_cliente = db.get_one("SELECT id from clientes WHERE nombre = 'David'")[0]
    
    db.execute("INSERT INTO loteria (numero, sorteo, año, precio) VALUES \
               (?, ?, ?, ?)", (10797, 1, 2025, 3))
    id_loteria = db.get_one("SELECT id from loteria WHERE numero = 10797")[0]
    
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO reservas_loteria_cliente (id_cliente, id_loteria, cantidad_decimos) VALUES \
               (?, ?, ?)", (id_cliente, id_loteria, 0),)