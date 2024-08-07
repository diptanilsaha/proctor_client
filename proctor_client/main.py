import os
import sys
from typing import List
from PyQt6.QtGui import QIcon
from PyQt6.QtSql import QSqlDatabase
from PyQt6.QtWidgets import QApplication, QMessageBox
from proctor_client.utils.database import LocalDatabase
from proctor_client.utils.rest_api import ProctorRestAPI
from proctor_client.admin_dialogs.admin import AdminMainWindow
from proctor_client.user_dialogs.password import VerifyPasswordDialog
from proctor_client.user_dialogs.tray import ProctorClientSystemTray
from proctor_client.utils.admin import isAdmin
from proctor_client.constants import WINDOW_TITLE, ICON, APP_DIR, LOCAL_DB

class ProctorClientApp(QApplication):
    def __init__(self, argv: List[str]) -> None:
        super().__init__(argv)

        self.setApplicationName('Proctor Client')
        self.setApplicationDisplayName('Proctor Client')
        self.setApplicationVersion('v1.1')

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

            vpd = VerifyPasswordDialog(password_hash)
            if not vpd.exec():
                dlg = QMessageBox()
                dlg.setWindowIcon(QIcon(ICON))
                dlg.setWindowTitle(WINDOW_TITLE)
                dlg.setText("Proctor Client could not start.")
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


