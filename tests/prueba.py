# from logic.user_manager import UserManager

# name = "Francisco"
# surnames = "Simon Lopez"
# phone = "697115860"

# um = UserManager()

# um.add_user(name, surnames, None, phone)
# print(um.get_users())
# um.close()









# import sys
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QLabel, QLineEdit, QPushButton,
#     QListWidget, QHBoxLayout, QVBoxLayout, QFormLayout, QMessageBox
# )

# class FormularioUsuarios(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Gestión de Usuarios")
#         self.setGeometry(100, 100, 600, 300)

#         # Layout principal: horizontal (izquierda y derecha)
#         layout_principal = QHBoxLayout()

#         # ----------- IZQUIERDA: Formulario -----------
#         layout_izquierda = QVBoxLayout()
#         layout_formulario = QFormLayout()

#         self.input_nombre = QLineEdit()
#         self.input_apellidos = QLineEdit()
#         self.input_email = QLineEdit()
#         self.input_telefono = QLineEdit()

#         layout_formulario.addRow("Nombre:", self.input_nombre)
#         layout_formulario.addRow("Apellidos:", self.input_apellidos)
#         layout_formulario.addRow("Email:", self.input_email)
#         layout_formulario.addRow("Teléfono:", self.input_telefono)

#         boton_añadir = QPushButton("Añadir usuario")
#         boton_añadir.clicked.connect(self.agregar_usuario)

#         layout_izquierda.addLayout(layout_formulario)
#         layout_izquierda.addWidget(boton_añadir)

#         # ----------- DERECHA: Lista de usuarios -----------
#         self.lista_usuarios = QListWidget()

#         # Añadir ambos lados al layout principal
#         layout_principal.addLayout(layout_izquierda, stretch=2)
#         layout_principal.addWidget(self.lista_usuarios, stretch=3)

#         self.setLayout(layout_principal)

#     def agregar_usuario(self):
#         nombre = self.input_nombre.text().strip()
#         apellidos = self.input_apellidos.text().strip()
#         email = self.input_email.text().strip()
#         telefono = self.input_telefono.text().strip()

#         if not (nombre and apellidos and email and telefono):
#             QMessageBox.warning(self, "Campos incompletos", "Por favor, rellena todos los campos.")
#             return

#         texto_usuario = f"{nombre} {apellidos} - {email} - {telefono}"
#         self.lista_usuarios.addItem(texto_usuario)

#         # Limpiar los campos después de añadir
#         self.input_nombre.clear()
#         self.input_apellidos.clear()
#         self.input_email.clear()
#         self.input_telefono.clear()

# # Ejecutar la app
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ventana = FormularioUsuarios()
#     ventana.show()
#     sys.exit(app.exec())


import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QPushButton, QLabel
)

# ----- Ventana secundaria -----
class VentanaSecundaria(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana secundaria")
        self.setGeometry(150, 150, 300, 150)

        layout = QVBoxLayout()
        label = QLabel("¡Hola! Soy la ventana secundaria.")
        layout.addWidget(label)

        self.setLayout(layout)

# ----- Ventana principal -----
class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ventana principal")
        self.setGeometry(100, 100, 400, 200)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        boton_abrir = QPushButton("Abrir ventana secundaria")
        boton_abrir.clicked.connect(self.abrir_ventana_secundaria)

        layout.addWidget(boton_abrir)
        central_widget.setLayout(layout)

        # Aquí guardamos la referencia a la ventana secundaria
        self.ventana_secundaria = None

    def abrir_ventana_secundaria(self):
        if self.ventana_secundaria is None:
            self.ventana_secundaria = VentanaSecundaria()
        self.ventana_secundaria.show()

# ----- Ejecutar app -----
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
