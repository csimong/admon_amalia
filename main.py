"""Main entry point for the application. It imports the GUI and the database and contains the logic for starting the app. """

import sys
from PyQt6.QtWidgets import QApplication
from application.landing.gui.app import MainWindow
from shared.database.database_manager import Database


def main():
    Database().init_database()

    # Initiate PyQt app
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    # Execute main app loop and exit when user close the window
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
