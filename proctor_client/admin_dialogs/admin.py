import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QWidget
)
from utils.database import LocalDatabase
from utils.rest_api import ProctorRestAPI
from admin_dialogs.password import SetPasswordDialog
from admin_dialogs.register import RegisterClientDialog
from constants import WINDOW_TITLE, ICON
import resources.makeqrc

class AdminMainWindow(QMainWindow):
    def __init__(self, db: LocalDatabase, rapi: ProctorRestAPI):
        super().__init__()

        self.db = db
        self.rapi = rapi
        self.setWindowTitle(f"Admin - {WINDOW_TITLE}")
        self.setWindowIcon(QIcon(ICON))
        self.setFixedSize(QSize(300, 200))

        main_window_layout = QVBoxLayout()

        admin_label = QLabel()
        admin_label.setText("Proctor Client")
        admin_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        admin_label.setFont(QFont('Arial', 30))

        copyright_label = QLabel()
        copyright_label.setText(f"Client Name: Not registered yet.")
        creds = db.get_credentials()
        if creds:
            copyright_label.setText(f"Client Name: {creds['client_name']}")
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_layout = QVBoxLayout()
        label_layout.addWidget(admin_label)
        label_layout.addWidget(copyright_label)

        button_layout = QHBoxLayout()

        self.password_button = QPushButton("Set/Change Password")
        self.password_button.setFixedHeight(40)
        self.password_button.clicked.connect(self.password_button_clicked)
        button_layout.addWidget(self.password_button)

        self.register_button = QPushButton("Register")
        self.register_button.setFixedHeight(40)
        self.register_button.clicked.connect(self.register_button_clicked)
        button_layout.addWidget(self.register_button)

        main_window_layout.addLayout(label_layout)
        main_window_layout.addLayout(button_layout)

        layout_widget = QWidget()
        layout_widget.setLayout(main_window_layout)
        self.setCentralWidget(layout_widget)

        self.setPasswordDialog = SetPasswordDialog(self.db)
        self.registerClientDialog = RegisterClientDialog(self.rapi)

    def password_button_clicked(self):
        if self.setPasswordDialog.exec():
            QMessageBox.information(self, "Success", "Proctor Client password set/changed successfully!")

    def register_button_clicked(self):
        creds = self.db.get_credentials()
        if not creds:
            if self.registerClientDialog.exec():
                QMessageBox.information(self, "Success", "Proctor Client registered successfully. Restart Proctor Client.")
                sys.exit(0)

        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle(f"Warning - {WINDOW_TITLE}")
            dlg.setText("Proctor Client is already registered. Do you want to register again?")
            dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            dlg.setIcon(QMessageBox.Icon.Warning)
            button = dlg.exec()

            if button == QMessageBox.StandardButton.Yes:
                if self.registerClientDialog.exec():
                    QMessageBox.information(self, "Success", "Proctor Client registered successfully. Restart Proctor Client.")
                    sys.exit(0)