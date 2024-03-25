import requests
from utils.database import LocalDatabase
from constants import USER_AGENT

class ProctorRestAPI:
    def __init__(self, db: LocalDatabase):
        self.db = db
        self.headers = {
            'User-Agent': USER_AGENT,
        }
        self.creds = None
        self.server_ip_addr = None
        self.server_port = None
        self.api_url = None
        self.token = None

    def init_creds(self):
        self.creds = self.db.get_credentials()

        if not self.creds:
            return False

        self.server_ip_addr = self.creds['server_ip_addr']
        self.server_port = self.creds['server_port']
        self.api_url = f"http://{self.server_ip_addr}:{self.server_port}/api/usbIncident/"
        self.token = self.creds['client_token']

        return True

    def register_client(
        self,
        server_ip_addr: str,
        server_port: int,
        client_name: str,
    ):
        api_url = f"http://{server_ip_addr}:{server_port}/api/clientRegister/"
        payload_data = {
            'client_name': client_name
        }

        try:
            r = requests.post(
                api_url,
                json=payload_data,
                headers=self.headers,
                timeout=2
            )
            if r.status_code != 201:
                return False

            data = r.json()
            token = data['token']

            update_db = self.db.update_credentials(
                server_ip_addr=server_ip_addr,
                server_port=server_port,
                client_name=client_name,
                client_token=token
            )

            return update_db
        except requests.exceptions.Timeout:
            return False

    def report_incident(self, status: str, device_info: str):
        if not self.init_creds():
            return False

        if status not in ['connection', 'disconnection']:
            return False

        try:
            payload_data = {
                'token': self.token,
                'status': status,
                'details': device_info
            }

            r = requests.post(
                self.api_url,
                json=payload_data,
                headers=self.headers,
                timeout=5
            )

            if r.status_code != 201:
                return False
        except requests.exceptions.ConnectTimeout:
            return False

        return True
