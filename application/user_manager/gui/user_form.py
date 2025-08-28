"""Scipts to manage GUI for user forms."""
from PyQt6.QtWidgets import (QLineEdit, QWidget, QPushButton, QMessageBox,
                             QHBoxLayout, QVBoxLayout, QFormLayout, QTableWidget,
                             QTableWidgetItem)
from application.user_manager.repository.user_repository import UserRepository
class UserManagerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Área de gestión de Usuarios")
        self.setGeometry(100, 100, 5000, 5000)
        self.setObjectName("user_manager_window")


        # Initialize User repository
        self.user_repository = UserRepository()
        
        # Create editing user id
        self.editing_user_id = None
        
        # main_layout: horizontal (left and right)
        main_layout = QHBoxLayout()
        
        # ----------- LEFT: Form -----------
        left_layout = QVBoxLayout()
        left_layout.setObjectName("left_layout")
        form_layout = QFormLayout()
        form_layout.setObjectName("left_form_layout")


        # Create user name, surnames, email and phone widgets
        self.input_name = QLineEdit()
        self.input_name.setObjectName("input_name_line_edit")
        self.input_surnames = QLineEdit()
        self.input_surnames.setObjectName("input_surnames_line_edit")
        self.input_email = QLineEdit()
        self.input_email.setObjectName("input_email_line_edit")
        self.input_phone = QLineEdit()
        self.input_phone.setObjectName("input_phone_line_edit")
        
        self.input_name.setPlaceholderText("Ej: David")
        self.input_surnames.setPlaceholderText("Ej: Bisbal")
        self.input_email.setPlaceholderText("Ej: davidbisbal@gmail.com")
        self.input_phone.setPlaceholderText("Ej: +34671345234")

        form_layout.addRow("Nombre:", self.input_name)
        form_layout.addRow("Apellidos:", self.input_surnames)
        form_layout.addRow("Email:", self.input_email)
        form_layout.addRow("Teléfono:", self.input_phone)


        # Save user data in database and refresh users in list widget
        self.btn_save = QPushButton("Guardar", self)
        self.btn_save.setObjectName("save_button")
        self.btn_save.clicked.connect(self.save_or_update_user)
        
        left_layout.addLayout(form_layout)
        left_layout.addWidget(self.btn_save)

        # ----------- RIGHT: List of users -----------
        self.table = QTableWidget()
        self.table.setObjectName("right_table_widget")
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Nombre", "Apellidos", "Email", "Teléfono", "Editar", "Borrar"])
        self.table.setColumnWidth(0, 200)
        self.table.setColumnWidth(1, 200)
        self.table.setColumnWidth(2, 200)
        self.table.setColumnWidth(3, 200)
        self.get_users()
        

        # Add both sides to main_layout
        main_layout.addLayout(left_layout, stretch=2)
        main_layout.addWidget(self.table, stretch=3)

        self.setLayout(main_layout)
        
        
    def save_or_update_user(self):
        name = self.input_name.text().strip()
        surnames = self.input_surnames.text().strip()
        email = self.input_email.text().strip()
        phone = self.input_phone.text().strip()
        
        if not name or not surnames:
            QMessageBox.warning(self, "Error", "Debes especificar nombre y apellidos del usuario.")
            return

        # Edit mode
        if self.editing_user_id:
            self.user_repository.update_user(self.editing_user_id, name, surnames, email, phone)
            print("Usuario actualizado:", name, surnames, email, phone)
            self.editing_user_id = None
            self.btn_save.setText("Guardar")
            
        # New user mode
        else:
            self.user_repository.add_user(name, surnames, email, phone)
            print("Usuario agregado:", name, surnames, email, phone)

        
        self.input_name.clear()
        self.input_surnames.clear()
        self.input_email.clear()
        self.input_phone.clear()
        self.get_users()
        
        
    def get_users(self):
        self.table.setRowCount(0)
        users = self.user_repository.get_users()
        for row_idx, (user_id, name, surnames, email, phone) in enumerate(users):
            self.table.insertRow(row_idx)
            self.table.setItem(row_idx, 0, QTableWidgetItem(name))
            self.table.setItem(row_idx, 1, QTableWidgetItem(surnames))
            self.table.setItem(row_idx, 2, QTableWidgetItem(email))
            self.table.setItem(row_idx, 3, QTableWidgetItem(phone))

            # Edit button
            btn_edit = QPushButton("Editar")
            btn_edit.clicked.connect(lambda _, uid=user_id: self.edit_user(uid))
            self.table.setCellWidget(row_idx, 4, btn_edit)
            
            # Delete button
            btn_delete = QPushButton("Borrar")
            btn_delete.clicked.connect(lambda _, uid=user_id: self.delete_user(uid))
            self.table.setCellWidget(row_idx, 5, btn_delete)
        
    def edit_user(self, user_id):
        user = self.user_repository.get_user_by_id(user_id)
        if user:
            print(user)
            _, name, surnames, email, phone = user

        self.input_name.setText(name)
        self.input_surnames.setText(surnames)
        self.input_email.setText(email)
        self.input_phone.setText(phone)
        
        self.editing_user_id = user_id
        self.btn_save.setText("Actualizar")
            
    def delete_user(self, user_id):
        answer = QMessageBox.question(
            self,
            "Confirmar eliminación",
            "¿Estás seguro de que quieres eliminar este usuario?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if answer == QMessageBox.StandardButton.Yes:
            self.user_repository.delete_user(user_id)
            self.get_users()
            
    def closeEvent(self, event):
        """This method is called when the user form window is being closed."""
        print("Closing connection to database...")
        self.user_repository.close()
        event.accept()

        