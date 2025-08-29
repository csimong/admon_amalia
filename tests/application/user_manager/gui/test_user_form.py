"""Tests for the user form script."""

from unittest.mock import patch, MagicMock
from PyQt6.QtWidgets import QLineEdit, QPushButton, QTableWidget, QMessageBox
from PyQt6.QtCore import Qt


from application.user_manager.gui.user_form import UserManagerWindow

## UNIT TESTS
@patch("application.user_manager.gui.user_form.UserRepository")
def test_user_manager_window_initializes_correctly(mock_repo_class, qtbot):
    """
    Tests the initialization of the UserManagerWindow.
    - Checks the window title and object name.
    - Checks the QLineEdits in the left form and right table widget are created.
    - Checks if the 'Guardar' button exists and has correct text.
    """
    # Mock UserRepository to avoid accessing real ddbb
    mock_repo = MagicMock()
    mock_repo.get_users.return_value = []
    mock_repo_class.return_value = mock_repo
    
    user_window = UserManagerWindow()
    qtbot.addWidget(user_window)
    
    # Verify window title and object name
    assert user_window.windowTitle() == "Área de gestión de Usuarios"
    assert user_window.objectName() == "user_manager_window"
    
    # Verify that QLineEdits exist
    input_name_line_edit = user_window.findChild(QLineEdit, "input_name_line_edit")
    input_surnames_line_edit = user_window.findChild(QLineEdit, "input_surnames_line_edit")
    input_email_line_edit = user_window.findChild(QLineEdit, "input_email_line_edit")
    input_phone_line_edit = user_window.findChild(QLineEdit, "input_phone_line_edit")
    
    assert input_name_line_edit is not None
    assert input_surnames_line_edit is not None
    assert input_email_line_edit is not None
    assert input_phone_line_edit is not None

    # Verify that save button exist
    save_button: QPushButton | None = user_window.findChild(QPushButton, "save_button") # type: ignore
    assert save_button is not None
    assert save_button.text() == "Guardar"

    # Verify that user table exist and has 
    table: QTableWidget | None = user_window.findChild(QTableWidget, "right_table_widget") # type: ignore
    assert table is not None
    assert table.columnCount() == 6
    assert table.horizontalHeaderItem(0).text() == "Nombre"
    assert table.horizontalHeaderItem(1).text() == "Apellidos"
    assert table.horizontalHeaderItem(2).text() == "Email"
    assert table.horizontalHeaderItem(3).text() == "Teléfono"
    assert table.horizontalHeaderItem(4).text() == "Editar"
    assert table.horizontalHeaderItem(5).text() == "Borrar"
    
    # Verify text can be properly written in QLineEdit
    name_input: QLineEdit | None = user_window.findChild(QLineEdit, "input_name_line_edit") # type: ignore
    assert name_input is not None
    qtbot.keyClicks(name_input, "Luis")
    assert name_input.text() == "Luis"
    

@patch("application.user_manager.gui.user_form.UserRepository")
def test_save_adds_user_if_valid(mock_repo_class, qtbot):
    """
    Tests that user is added if arguments are valid.
    """
    mock_repo = MagicMock()
    mock_repo.get_users.return_value = []
    mock_repo_class.return_value = mock_repo

    window = UserManagerWindow()
    qtbot.addWidget(window)

    window.input_name.setText("Luis")
    window.input_surnames.setText("Soler")
    window.input_email.setText("luis@example.com")
    window.input_phone.setText("123456789")

    qtbot.mouseClick(window.btn_save, Qt.MouseButton.LeftButton)

    mock_repo.add_user.assert_called_once_with("Luis", "Soler", "luis@example.com", "123456789")

@patch("application.user_manager.gui.user_form.UserRepository")
@patch("application.user_manager.gui.user_form.QMessageBox.warning")
def test_save_without_required_fields_shows_warning(mock_warning, mock_repo_class, qtbot):
    """
    Tests that trying to save user without required fields shows a warning.
    """
    mock_repo = MagicMock()
    mock_repo_class.return_value = mock_repo
    
    window = UserManagerWindow()
    qtbot.addWidget(window) 
    
    window.input_name.setText("")
    window.input_surnames.setText("")
    
    # Simulate the left click
    qtbot.mouseClick(window.btn_save, Qt.MouseButton.LeftButton)  
      
    mock_warning.assert_called_once()  

@patch("application.user_manager.gui.user_form.UserRepository")
def test_get_users_populates_table_correctly(mock_repo_class, qtbot):
    """
    Tests that get_users populates the right user table correctly.
    """
    # Mock user data
    mock_users = [
        (1, "David", "Bisbal", "davidbisbal@gmail.com", "+34671345234"),
        (2, "Tomatito", "Fernández", "tomatitofernandez@gmail.com", "+34671345237"),
    ]
    
    mock_repo = MagicMock()
    mock_repo.get_users.return_value = mock_users
    mock_repo_class.return_value = mock_repo

    window = UserManagerWindow()
    qtbot.addWidget(window)

    window.get_users()

    table = window.table

    # Verify number of rows
    assert table.rowCount() == 2

    # Verify cell content
    assert table.item(0, 0).text() == "David"
    assert table.item(0, 1).text() == "Bisbal"
    assert table.item(0, 2).text() == "davidbisbal@gmail.com"
    assert table.item(0, 3).text() == "+34671345234"

    assert table.item(1, 0).text() == "Tomatito"
    assert table.item(1, 1).text() == "Fernández"
    assert table.item(1, 2).text() == "tomatitofernandez@gmail.com"
    assert table.item(1, 3).text() == "+34671345237"

    # Verify that buttons "Editar" and "Borrar" exist
    for row in range(2):
        edit_btn = table.cellWidget(row, 4)
        delete_btn = table.cellWidget(row, 5)

        assert isinstance(edit_btn, QPushButton)
        assert edit_btn.text() == "Editar"

        assert isinstance(delete_btn, QPushButton)
        assert delete_btn.text() == "Borrar"


@patch("application.user_manager.gui.user_form.UserRepository")
def test_edit_user_loads_fields(mock_repo_class, qtbot):
    """
    Tests that edit user mode loads user fields properly.
    """
    mock_repo = MagicMock()
    mock_repo.get_users.return_value = []
    mock_repo.get_user_by_id.return_value = (1, "Luis", "Soler", "luis@example.com", "123456789")
    mock_repo_class.return_value = mock_repo

    window = UserManagerWindow()
    qtbot.addWidget(window)

    window.edit_user(1)

    assert window.input_name.text() == "Luis"
    assert window.input_surnames.text() == "Soler"
    assert window.input_email.text() == "luis@example.com"
    assert window.input_phone.text() == "123456789"
    assert window.btn_save.text() == "Actualizar"
    assert window.editing_user_id == 1
    
@patch("application.user_manager.gui.user_form.QMessageBox.question", return_value=QMessageBox.StandardButton.Yes)
@patch("application.user_manager.gui.user_form.UserRepository")
def test_delete_user_confirmation_yes(mock_repo_class, mock_question, qtbot):
    """
    Tests that a user is properly deleted if answer to QMessageBox is yes.
    """
    mock_repo = MagicMock()
    mock_repo.get_users.return_value = []
    mock_repo_class.return_value = mock_repo

    window = UserManagerWindow()
    qtbot.addWidget(window)

    window.delete_user(42)

    mock_repo.delete_user.assert_called_once_with(42)
    mock_repo.get_users.assert_called()
    

@patch("application.user_manager.gui.user_form.QMessageBox.question", return_value=QMessageBox.StandardButton.No)
@patch("application.user_manager.gui.user_form.UserRepository")
def test_delete_user_confirmation_no(mock_repo_class, mock_question, qtbot):
    """
    Tests that a user is not deleted if answer to QMessageBox is no.
    """ 
    mock_repo = MagicMock()
    mock_repo.get_users.return_value = []
    mock_repo_class.return_value = mock_repo

    window = UserManagerWindow()
    qtbot.addWidget(window)

    window.delete_user(42)

    mock_repo.delete_user.assert_not_called()
