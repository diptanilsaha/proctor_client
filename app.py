import sys
from proctor_client.main import ProctorClientApp

if __name__ == "__main__":
    app = ProctorClientApp(sys.argv)
    app.exec()
