import os
from PyQt6.QtCore import QStandardPaths

APP_NAME = 'ProctorClient'
USER_AGENT = 'ProctorAdminClient'
APP_DATA_DIR = QStandardPaths.writableLocation(
    QStandardPaths.StandardLocation.AppDataLocation
)
APP_DIR = os.path.join(APP_DATA_DIR, APP_NAME)
LOG_FILE_DIR = os.path.join(APP_DIR, "logfiles")
LOCAL_DB = os.path.join(APP_DIR, "proctorclient.sqlite")
WINDOW_TITLE = 'Proctor Client'
ICON = ":/icons/favicon"
