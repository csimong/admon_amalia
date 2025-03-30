"""Main window configuration. It creates the main app window."""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel


class MyApp(QMainWindow):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mi Aplicación PyQt")
        self.setGeometry(100, 100, 400, 300)

        label = QLabel("¡Hola, PyQt!", self)
        label.move(150, 130)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())