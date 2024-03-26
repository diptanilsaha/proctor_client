from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QIcon
from proctor_client.utils.password import generate_password_hash
from proctor_client.utils.database import LocalDatabase
from proctor_client.constants import WINDOW_TITLE, ICON
import proctor_client.resources.makeqrc

class SetPasswordDialog(QDialog):
    def __init__(self, db: LocalDatabase):
        super().__init__()
        self.setWindowTitle(f"Set Client Password - {WINDOW_TITLE}")
        self.setWindowIcon(QIcon(ICON))
        password_layout = QVBoxLayout()

        self.password_label = QLabel(self)
        self.password_label.setText('Password')
        password_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input)

        confirm_password_layout = QVBoxLayout()

        self.confirm_password_label = QLabel(self)
        self.confirm_password_label.setText('Confirm Password')
        confirm_password_layout.addWidget(self.confirm_password_label)

        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        confirm_password_layout.addWidget(self.confirm_password_input)

        button_layout = QHBoxLayout()

        self.set_password_button = QPushButton("Set/Change Password")
        self.set_password_button.clicked.connect(self.set_password)
        button_layout.addWidget(self.set_password_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_operation)
        button_layout.addWidget(self.cancel_button)

        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(password_layout)
        dialog_layout.addLayout(confirm_password_layout)
        dialog_layout.addLayout(button_layout)

        self.setLayout(dialog_layout)

        self.db = db

    def set_password(self):
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if len(password) < 8:
            QMessageBox.critical(self, "Error", "Password cannot be less than 8 characters!")
        elif password != confirm_password:
            QMessageBox.critical(self, "Error", "Password did not match!")
        else:
            self.db.update_password(generate_password_hash(password))
            self.accept()

    def cancel_operation(self):
        self.reject()

