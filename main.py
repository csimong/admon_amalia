"""Main entry point for the application. It imports the GUI and the database and contains the logic for starting the app. """

import sys
from PyQt6.QtWidgets import QApplication
from gui.app import MyApp
from database.database import Database


def main():
    # Initiate database
    db = Database()
    with open("database/schema.sql", "r") as f:
        db.cursor.executescript(f.read())
        db.conn.commit()
    db.close()

    # Initiate PyQt app
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()

    # Execute main app loop and exit when user close the window
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
