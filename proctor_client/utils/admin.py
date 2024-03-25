import os
import sys

def isAdmin() -> bool:
    platform = sys.platform

    if platform.startswith('linux'):
        if os.environ.get("SUDO_UID") and os.geteuid() == 0:
            return True
        return False

    if platform.startswith('win'):
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())

    return False
