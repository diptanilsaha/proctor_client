import os
import sys
from typing import List
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QApplication, QMessageBox
from utils.database import LocalDatabase
from utils.rest_api import ProctorRestAPI
from admin_dialogs.admin import AdminMainWindow
from user_dialogs.tray import ProctorClientSystemTray
from utils.admin import isAdmin
from constants import WINDOW_TITLE, ICON, APP_DIR, LOCAL_DB

class MyApp(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)

        if not os.path.exists(APP_DIR):
            os.mkdir(APP_DIR)

        self.con = QSqlDatabase.addDatabase("QSQLITE")
        self.database_name = LOCAL_DB
        self.con.setDatabaseName(self.database_name)
        self.con.open()

        self.db = LocalDatabase(self.con)
        self.rapi = ProctorRestAPI(self.db)
        creds = self.db.get_credentials()
        password_hash = self.db.get_password()

        if isAdmin():
            self.admin_main_window = AdminMainWindow(
                self.db,
                self.rapi
            )
            self.admin_main_window.show()
        else:
            if not creds and not password_hash:
                dlg = QMessageBox()
                dlg.setWindowIcon(QIcon(ICON))
                dlg.setWindowTitle(WINDOW_TITLE)
                dlg.setText("Proctor Client - Client Password and Credentials not set.")
                dlg.setStandardButtons(QMessageBox.StandardButton.Ok)
                dlg.setIcon(QMessageBox.Icon.Critical)
                dlg.exec()
                sys.exit(0)
            self.setQuitOnLastWindowClosed(False)
            self.tray = ProctorClientSystemTray(
                self.db,
                self.rapi,
                creds,
                password_hash
            )
            self.tray.show()

if __name__ == "__main__":
    app = MyApp(sys.argv)
    app.exec()
