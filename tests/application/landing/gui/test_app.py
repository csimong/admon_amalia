"""Tests for the main application window."""

from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from pytestqt.qtbot import QtBot


from application.landing.gui.app import MainWindow

## UNIT TESTS
def test_main_window_initializes_correctly(qtbot: QtBot) -> None:
    """
    Tests the initialization of the MainWindow.
    - Checks the window title and object name.
    - Checks if the 'Gestor de Usuarios' button exists and has correct text.
    """
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == "ADMON AMALIA Gestor de Cuentas"
    assert window.objectName() == "main_window"
    
    central_widget = window.findChild(type(window.centralWidget()), "central_widget")
    assert central_widget is not None
    
    button: QPushButton | None = window.findChild(QPushButton, "open_user_manager_button") # type: ignore
    assert button is not None
    assert button.text() == "Gestor de Usuarios"


@patch("application.landing.gui.app.UserManagerWindow")
def test_open_user_manager_window_opens_after_click(mock_user_manager_window: MagicMock, qtbot: QtBot) -> None:
    """
    Tests that clicking the button is instantiated and shows the UserManagerWindow.
    """
    window = MainWindow()
    qtbot.addWidget(window)

    # Search for the button
    button = window.findChild(QPushButton, "open_user_manager_button")
    assert button is not None

    # Simulate the left click
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # Verify that UserManagerWindow is instantiated
    mock_user_manager_window.assert_called_once()

    # Verify that .show() was called in the instance
    instance = mock_user_manager_window.return_value
    instance.show.assert_called_once()


@patch("application.landing.gui.app.UserManagerWindow")
def test_open_user_manager_window_opens_only_once(mock_user_manager_window: MagicMock, qtbot: QtBot):
    """
    Tests that clicking the button several times is instantiated and shows the UserManagerWindow just once.
    """
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Simulate the left click twice
    button = window.findChild(QPushButton, "open_user_manager_button")
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)
    
    # Verify that UserManagerWindow is instantiated only once
    mock_user_manager_window.assert_called_once()
    
    # Verify that .show() was called in the instance twice
    mock_instance = mock_user_manager_window.return_value
    assert mock_instance.show.call_count == 2