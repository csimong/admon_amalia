"""Tests for the user manager repository."""

import sqlite3
import pytest
from application.user_manager.repository.user_repository import UserRepository
from shared.database.database_manager import Database


# INTEGRATION TESTS
@pytest.fixture
def user_repository():
    """
    Create an instance of the UserRepository class for testing.
    """
    repo = UserRepository()
    repo.db = Database(":memory:")
    repo.db.init_database()
    yield repo
    repo.close()

# UNIT TESTS
def test_close_closes_connection(user_repository):
    """
    Tests that the close function closes the connection to the database.
    """
    user_repository.close()
    with pytest.raises(sqlite3.ProgrammingError):
        user_repository.db.execute("CREATE TABLE test (id INTEGER)")


# INTEGRATION TESTS
def test_add_user_inserts_new_user_into_clientes_table(user_repository):
    """
    Tests that a new user can be added to the Clientes table.
    """
    
    user_repository.add_user("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    users = user_repository.get_users()
    assert len(users) == 1
    assert  users[0] == (1, "David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    
def test_get_users_returns_all_users_from_clientes_table(user_repository):
    """
    Tests that all users can be retrieved from the Clientes table.
    """
    user_repository.add_user("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    user_repository.add_user("Tomatito", "Fernández", "tomatitofernandez@gmail.com", "+34671345237")
    users = user_repository.get_users()
    assert len(users) == 2
    assert  users[0] == (1, "David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    assert  users[1] == (2, "Tomatito", "Fernández", "tomatitofernandez@gmail.com", "+34671345237")

def test_get_user_by_id_returns_correct_user(user_repository):
    """
    Tests that a user can be retrieved from the Clientes table by id.
    """
    user_repository.add_user("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    user_id = user_repository.get_users()[0][0]
    user = user_repository.get_user_by_id(user_id)
    assert user == (1, "David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    
def test_get_user_by_id_returns_none_if_user_does_not_exist(user_repository):
    assert user_repository.get_user_by_id(1) == None
    
def test_update_user_updates_user_in_clientes_table(user_repository):
    """
    Tests that a user can be updated in the Clientes table.
    """
    user_repository.add_user("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    user_id = user_repository.get_users()[0][0]
    user_repository.update_user(user_id, "Tomatito", "Fernández", "tomatitofernandez@gmail.com", "+34671345237")
    user = user_repository.get_user_by_id(user_id)
    assert user == (1, "Tomatito", "Fernández", "tomatitofernandez@gmail.com", "+34671345237")

def test_update_user_raise_error_if_param_is_missing(user_repository):
    """
    Tests that a user can be updated in the Clientes table.
    """
    user_repository.add_user("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    user_id = user_repository.get_users()[0][0]
    with pytest.raises(TypeError):
        user_repository.update_user(user_id, "Tomatito", "Fernández")

def test_delete_user_deletes_user_from_clientes_table(user_repository):
    """
    Tests that a user can be deleted from the Clientes table.
    """
    user_repository.add_user("David", "Bisbal", "davidbisbal@gmail.com", "+34671345234")
    user_id = user_repository.get_users()[0][0]
    user_repository.delete_user(user_id)
    assert user_repository.get_user_by_id(user_id) == None   