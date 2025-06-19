"""Scipts to manage GUI for user forms."""
from PyQt6.QtWidgets import (QLabel, QLineEdit, QWidget, QPushButton, QMessageBox,
                             QHBoxLayout, QVBoxLayout, QFormLayout, QListWidget)
from application.user_manager.repository.user_repository import UserRepository
class UserManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Área de gestión de Usuarios")
        self.setGeometry(100, 100, 600, 300)

        # Initialize User repository
        self.user_repository = UserRepository()
        
        # main_layout: horizontal (left and right)
        main_layout = QHBoxLayout()
        
        # ----------- LEFT: Form -----------
        left_layout = QVBoxLayout()
        form_layout = QFormLayout()

        # Create user name, surnames, email and phone widgets
        self.input_name = QLineEdit()
        self.input_surnames = QLineEdit()
        self.input_email = QLineEdit()
        self.input_phone = QLineEdit()
        
        self.input_name.setPlaceholderText("Ej: David")
        self.input_surnames.setPlaceholderText("Ej: Bisbal")
        self.input_email.setPlaceholderText("Ej: davidbisbal@gmail.com")
        self.input_phone.setPlaceholderText("Ej: +34671345234")

        form_layout.addRow("Nombre:", self.input_name)
        form_layout.addRow("Apellidos:", self.input_surnames)
        form_layout.addRow("Email:", self.input_email)
        form_layout.addRow("Teléfono:", self.input_phone)


        # Save user data in database
        self.btn_save = QPushButton("Guardar", self)
        self.btn_save.clicked.connect(self.add_user)
        self.btn_save.clicked.connect(self.get_user)
        
        left_layout.addLayout(form_layout)
        left_layout.addWidget(self.btn_save)

        # ----------- RIGHT: List of users -----------
        self.list_users = QListWidget()
        self.list_users.addItem(self.get_user())

        # Add both sides to main_layout
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addWidget(self.list_users, stretch=3)

        self.setLayout(main_layout)

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

    def get_user(self):
        users = self.user_repository.get_users()
        self.list_users.clear()
        for user in users:
            user_item = f"{user[1]} {user[2]}; {user[3]}; {user[4]}"
            self.list_users.addItem(user_item)

        