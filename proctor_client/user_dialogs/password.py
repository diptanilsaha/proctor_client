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
from utils.password import check_password_hash
from constants import WINDOW_TITLE, ICON
import resources.makeqrc

class VerifyPasswordDialog(QDialog):
    def __init__(self, password_hash):
        super().__init__()
        self.setWindowTitle(f"Verify Password - {WINDOW_TITLE}")
        self.setWindowIcon(QIcon(ICON))
        password_layout = QVBoxLayout()

        self.password_label = QLabel(self)
        self.password_label.setText('Password')
        password_layout.addWidget(self.password_label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input)

        button_layout = QHBoxLayout()

        self.verify_password_button = QPushButton("Confirm")
        self.verify_password_button.clicked.connect(self.verify_password)
        button_layout.addWidget(self.verify_password_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_operation)
        button_layout.addWidget(self.cancel_button)

        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(password_layout)
        dialog_layout.addLayout(button_layout)

        self.setLayout(dialog_layout)

        self.password_hash = password_hash

    def verify_password(self):
        password = self.password_input.text()

        if not check_password_hash(password, self.password_hash):
            QMessageBox.critical(self, "Error", "Incorrect Password!")
            self.reject()
        else:
            self.accept()

    def cancel_operation(self):
        self.reject()
