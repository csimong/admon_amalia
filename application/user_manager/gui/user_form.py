"""Scipts to manage GUI for user forms."""
from PyQt6.QtWidgets import QLabel, QLineEdit, QWidget, QPushButton, QMessageBox
from application.user_manager.repository.user_repository import UserRepository
class UserManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Área de gestión de Usuarios")
        self.setGeometry(100, 100, 600, 300)

        # Initialize User manager
        self.user_repository = UserRepository()

        # Create user name widgets
        self.label_name = QLabel("Nombre:", self)
        self.label_name.move(20, 30)
        self.input_name = QLineEdit(self)
        self.input_name.setPlaceholderText("Ej: David")
        self.input_name.move(100, 30)

        # Create user surnames widgets
        self.label_surnames = QLabel("Apellidos:", self)
        self.label_surnames.move(20, 70)
        self.input_surnames = QLineEdit(self)
        self.input_surnames.setPlaceholderText("Ej: Bisbal")
        self.input_surnames.move(100, 70)

        # Create user email widgets
        self.label_email = QLabel("Email:", self)
        self.label_email.move(20, 110)
        self.input_email = QLineEdit(self)
        self.input_email.setPlaceholderText("Ej: davidbisbal@gmail.com")
        self.input_email.move(100, 110)

        # Create user phone widgets
        self.label_phone = QLabel("Teléfono:", self)
        self.label_phone.move(20, 150)
        self.input_phone = QLineEdit(self)
        self.input_phone.setPlaceholderText("Ej: +34671345234")
        self.input_phone.move(100, 150)

        # Save user data in database
        self.btn_save = QPushButton("Guardar", self)
        self.btn_save.move(100, 190)
        self.btn_save.clicked.connect(self.add_user)

    def add_user(self):
        name = self.input_name.text()
        surnames = self.input_surnames.text()
        email = self.input_email.text()
        phone = self.input_phone.text()
        if name and surnames:
            self.user_repository.add_user(name, surnames, email, phone)
            print("Usuario agregado:", name, surnames, email, phone)
        else:
            QMessageBox.warning(
                self, "Error", "Debes especificar nombre y apellidos del usuario.")