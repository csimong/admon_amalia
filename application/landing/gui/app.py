"""Landing Page window configuration. It creates the main app window."""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout
from application.user_manager.gui.user_form import UserManagerWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ADMON AMALIA Gestor de Cuentas ")
        self.setGeometry(100, 100, 600, 300)
        
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        open_user_manager_button = QPushButton("Gestor de Usuarios")
        open_user_manager_button.clicked.connect(self.open_user_manager_window)
        
        layout.addWidget(open_user_manager_button)
        central_widget.setLayout(layout)
        
        self.user_manager_window = None
        
        
    def open_user_manager_window(self):
        if self.user_manager_window is None:
            self.user_manager_window = UserManagerWindow()
        self.user_manager_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
