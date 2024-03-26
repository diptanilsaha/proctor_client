import sys
import socketio
from PyQt6.QtCore import QThreadPool
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from usbmonitor import USBMonitor
from proctor_client.user_dialogs.password import VerifyPasswordDialog
from proctor_client.utils.database import LocalDatabase
from proctor_client.utils.rest_api import ProctorRestAPI
from proctor_client.constants import WINDOW_TITLE, ICON
from proctor_client.utils.worker import Worker
import proctor_client.resources.makeqrc

class ProctorClientSystemTrayMenu(QMenu):
    def __init__(self):
        super().__init__()

        self.activate_action = QAction(self)
        self.activate_action.setText("Activate")

        self.deactivate_action = QAction(self)
        self.deactivate_action.setText("Deactivate")
        self.deactivate_action.setEnabled(False)

        self.exit = QAction(self)
        self.exit.setText("Exit")

        self.addActions([
            self.activate_action,
            self.deactivate_action,
            self.exit
        ])


class ProctorClientSystemTray(QSystemTrayIcon):
    def __init__(
        self,
        db: LocalDatabase,
        rapi: ProctorRestAPI,
        creds: dict,
        password_hash: str
    ):
        super().__init__()

        self.sio = socketio.Client(reconnection=False)
        self.rapi = rapi
        self.creds = creds
        self.db = db

        self.setIcon(QIcon(ICON))
        self.setVisible(True)
        self.password_hash = password_hash

        self.menu = ProctorClientSystemTrayMenu()
        self.setContextMenu(self.menu)

        self.menu.activate_action.triggered.connect(self.activate_clicked)
        self.menu.deactivate_action.triggered.connect(self.deactivate_clicked)
        self.menu.exit.triggered.connect(self.on_exit_trigger)

        self.activate_click = False
        self.usbMonitor = USBMonitor()

        @self.sio.event
        def connect():
            self.menu.activate_action.setEnabled(False)
            self.menu.deactivate_action.setEnabled(True)
            self.menu.exit.setEnabled(False)
            self.usbMonitor.start_monitoring(
                on_connect=self.on_usb_connect,
                on_disconnect=self.on_usb_disconnect
            )

        @self.sio.event
        def disconnect():
            self.usbMonitor.stop_monitoring()
            self.menu.activate_action.setEnabled(True)
            self.menu.deactivate_action.setEnabled(False)
            self.menu.exit.setEnabled(True)
            self.activate_click = False

            self.showMessage(
                "Disconnected",
                "Proctor Client disconnected from Proctor Server.",
                QSystemTrayIcon.MessageIcon.Warning,
                1000
            )

        self.threadpool = QThreadPool()

    def socketio_connect(self):
        url = f"http://{self.creds['server_ip_addr']}:{self.creds['server_port']}/"
        token = self.creds['client_token']
        self.sio.connect(url, auth=token)

    def deactivate_clicked(self):
        verify_pass_dialog = VerifyPasswordDialog(self.password_hash)
        if verify_pass_dialog.exec():
            self.sio.disconnect()

    def activate_clicked(self):
        if self.activate_click:
            self.showMessage(
                "Connecting...",
                "Proctor Client is trying to connect with Proctor Server.",
                QSystemTrayIcon.MessageIcon.Warning,
                1000
            )
            return

        verify_pass_dialog = VerifyPasswordDialog(self.password_hash)
        if verify_pass_dialog.exec():
            self.activate_click = True
            worker = Worker(self.socketio_connect)
            worker.signals.finished.connect(self.socketio_connected)
            worker.signals.error.connect(self.socketio_connection_error)

            self.threadpool.start(worker)
            self.showMessage(
                "Connecting...",
                "Proctor Client is trying to connect with Proctor Server.",
                QSystemTrayIcon.MessageIcon.Warning,
                1000
            )

    def socketio_connection_error(self):
        self.showMessage(
            "Connection Error",
            "Proctor Client could not connect with Proctor Server.",
            QSystemTrayIcon.MessageIcon.Critical,
            1000
        )
        self.activate_click = False

    def socketio_connected(self):
        self.showMessage(
            "Connected",
            "Proctor Client is now connected with Proctor Server.",
            QSystemTrayIcon.MessageIcon.Information,
            1000
        )

    def on_exit_trigger(self):
        verify_pass_dialog = VerifyPasswordDialog(self.password_hash)
        if verify_pass_dialog.exec():
            self.showMessage(
                f"{WINDOW_TITLE}",
                "Proctor Client Terminated.",
                QSystemTrayIcon.MessageIcon.Information,
                1000
            )
            sys.exit(0)

    def on_usb_connect(self, device_id, device_info):
        status = 'connection'
        device_details = ProctorClientSystemTray.device_info_str(device_info)
        self.rapi.report_incident(
            status,
            f"Connected: ({device_details})"
        )

    def on_usb_disconnect(self, device_id, device_info):
        status = 'disconnection'
        device_details = ProctorClientSystemTray.device_info_str(device_info)
        self.rapi.report_incident(
            status,
            f"Disconnected: {device_details}"
        )

    @staticmethod
    def device_info_str(device_info):
        return f"Model: {device_info['ID_MODEL']}; Dev Name: {device_info['DEVNAME']}"
