"""Tests for the user form script."""

import pytest
from unittest.mock import patch, MagicMock
from application.user_manager.repository.user_repository import UserRepository
from shared.database.database_manager import Database

from application.user_manager.gui.user_form import UserManagerWindow

## UNIT TESTS
@patch("application.user_manager.gui.user_form.UserRepository")
def test_user_manager_window_initializes_correctly(mock_repo_class, qtbot):
    """
    Tests the initialization of the UserManagerWindow.
    - Checks the window title and object name.
    - Checks the main layout, left form and right table widget are created.
    - Checks if the 'Guardar' button exists and has correct text.
    """
    # Mock UserRepository to avoid accessing real ddbb
    mock_repo = MagicMock()
    mock_repo.get_users.return_value = []
    mock_repo_class.return_value = mock_repo
    
    user_window = UserManagerWindow()
    qtbot.addWidget(user_window)
    
    assert user_window.windowTitle() == "Área de gestión de Usuarios"
    assert user_window.objectName() == "user_manager_window"
    
    left_layout = user_window.findChild(type(user_window.layout().itemAt(0)), "left_layout")
    assert left_layout is not None
    
    ############TODO: continue



