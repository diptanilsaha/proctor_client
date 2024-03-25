import ipaddress
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QLabel,
    QPushButton,
    QMessageBox
)
from PyQt6.QtGui import QIntValidator, QIcon
from utils.rest_api import ProctorRestAPI
from constants import WINDOW_TITLE, ICON
import resources.makeqrc

class RegisterClientDialog(QDialog):
    def __init__(self, rapi: ProctorRestAPI):
        super().__init__()
        self.setWindowTitle(f"Register - {WINDOW_TITLE}")
        self.setWindowIcon(QIcon(ICON))
        server_ip_layout = QVBoxLayout()

        self.server_ip_label = QLabel()
        self.server_ip_label.setText("Server IP Address")
        server_ip_layout.addWidget(self.server_ip_label)

        self.server_ip_text = QLineEdit()
        self.server_ip_text.setEchoMode(QLineEdit.EchoMode.Normal)
        server_ip_layout.addWidget(self.server_ip_text)

        server_port_layout = QVBoxLayout()

        self.server_port_label = QLabel()
        self.server_port_label.setText("Server Port")
        server_port_layout.addWidget(self.server_port_label)

        self.server_port_text = QLineEdit()
        self.server_port_text.setEchoMode(QLineEdit.EchoMode.Normal)
        server_port_layout.addWidget(self.server_port_text)

        server_port_validator = QIntValidator()
        server_port_validator.setRange(0, 65565)
        self.server_port_text.setValidator(server_port_validator)

        client_name_layout = QVBoxLayout()

        self.client_name_label = QLabel()
        self.client_name_label.setText("Client Name")
        client_name_layout.addWidget(self.client_name_label)

        self.client_name_text = QLineEdit()
        self.client_name_text.setEchoMode(QLineEdit.EchoMode.Normal)
        client_name_layout.addWidget(self.client_name_text)

        button_layout = QHBoxLayout()

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.clicked.connect(self.confirm_operation)
        button_layout.addWidget(self.confirm_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_operation)
        button_layout.addWidget(self.cancel_button)

        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(server_ip_layout)
        dialog_layout.addLayout(server_port_layout)
        dialog_layout.addLayout(client_name_layout)
        dialog_layout.addLayout(button_layout)

        self.setLayout(dialog_layout)

        self.rapi = rapi

    def confirm_operation(self):
        ip_addr = self.server_ip_text.text()
        port = self.server_port_text.text()
        client_name = self.client_name_text.text()

        if not ip_addr:
            QMessageBox.critical(self, "Error", "Server IP Address cannot be left blank.")
            return

        if not port:
            QMessageBox.critical(self, "Error", "Server Port cannot be left blank.")
            return

        if not client_name:
            QMessageBox.critical(self, "Error", "Client Name cannot be left blank.")
            return

        validate_ip = RegisterClientDialog.validate_ip_address(ip_addr)
        validate_cn = RegisterClientDialog.validate_client_name(client_name)

        if validate_ip and validate_cn and port:
            register = self.rapi.register_client(
                server_ip_addr=ip_addr,
                server_port=int(port),
                client_name=client_name
            )
            if register:
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Proctor Client could not be registered.")

        else:
            if validate_ip:
                QMessageBox.critical(self, "Error", "Client Name could not be validated.")
            elif validate_cn:
                QMessageBox.critical(self, "Error", "Server IP Address could not be validated.")

    def cancel_operation(self):
        self.reject()

    @staticmethod
    def validate_ip_address(ip_addr: str) -> bool:
        try:
            ipaddress.ip_address(ip_addr)
            return True
        except:
            return False

    @staticmethod
    def validate_client_name(client_name: str) -> bool:
        l = client_name.split('.')
        if len(l) != 3:
            return False
        for i in l:
            length = len(i)
            if length > 0 and length <= 10:
                continue
            else:
                return False

        return True
