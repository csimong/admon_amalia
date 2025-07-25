"""Tests for the main application window."""

from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtCore import Qt
from pytestqt.qtbot import QtBot


from application.landing.gui.app import MainWindow


def test_main_window_init(qtbot: QtBot) -> None:
    """
    Tests the initialization of the MainWindow.
    - Checks the window title.
    - Checks if the 'Gestor de Usuarios' button exists and has correct text.
    """
    window = MainWindow()
    qtbot.addWidget(window)

    assert window.windowTitle() == "ADMON AMALIA Gestor de Cuentas "

    # Search for the button using its name
    button: QPushButton | None = window.findChild(QPushButton, "open_user_manager_button") # type: ignore
    assert button is not None
    assert button.text() == "Gestor de Usuarios"


@patch("application.landing.gui.app.UserManagerWindow")
def test_open_user_manager_window_click(mock_user_manager_cls: MagicMock, qtbot: QtBot) -> None:
    """
    Tests that clicking the button instantiates and shows the UserManagerWindow.
    """
    window = MainWindow()
    qtbot.addWidget(window)

    # Search for the button
    button = window.findChild(QPushButton, "open_user_manager_button")
    assert button is not None

    # Simulate the left click
    qtbot.mouseClick(button, Qt.MouseButton.LeftButton)

    # Verify that UserManagerWindow instantiated
    mock_user_manager_cls.assert_called_once()

    # Verify that .show() was called in the instance
    instance = mock_user_manager_cls.return_value
    instance.show.assert_called_once()
