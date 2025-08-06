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


## INTEGRATION TESTS
