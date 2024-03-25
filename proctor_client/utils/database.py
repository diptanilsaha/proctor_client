import datetime
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

class LocalDatabase:
    def __init__(self, con: QSqlDatabase):
        self.con = con
        self.create_database_and_table()

    def create_database_and_table(self):

        create_table_query = QSqlQuery(self.con)
        tables = self.con.tables()

        if 'password' not in tables:
            create_table_query.exec(
                """
                CREATE TABLE password(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    password_hash CHAR(120) NOT NULL,
                    last_updated DATETIME NOT NULL
                )
                """
            )

        if 'connection_credential' not in tables:
            create_table_query.exec(
                """
                CREATE TABLE connection_credential(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    server_ip_addr CHAR(15) NOT NULL,
                    server_port INT NOT NULL,
                    client_name VARCHAR(40) NOT NULL,
                    client_token TEXT NOT NULL
                )
                """
            )

        if 'log' not in tables:
            create_table_query.exec(
                """
                CREATE TABLE log(
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                    session_id CHAR(20) NOT NULL,
                    details TEXT NOT NULL
                    timestamp DATETIME NOT NULL,
                )
                """
            )

        return True

    def set_password(self, password_hash):
        insert_pass_query = QSqlQuery(self.con)

        insert_pass_query.prepare(
            """
            INSERT INTO password (
                password_hash, last_updated
            ) VALUES (?, ?)
            """
        )

        insert_pass_query.addBindValue(password_hash)
        insert_pass_query.addBindValue(
            datetime.datetime.now().replace(microsecond=0)
        )

        return insert_pass_query.exec()

    def get_password(self):
        get_pass_query = QSqlQuery(self.con)

        get_pass_query.prepare(
            """
                SELECT password_hash FROM password
            """
        )

        get_pass_query.exec()

        if get_pass_query.first():
            return get_pass_query.value(0)

        return None

    def update_password(self, password_hash):
        update_pass_query = QSqlQuery(self.con)

        if not self.get_password():
            return self.set_password(password_hash)

        update_pass_query.prepare(
            """
            UPDATE password SET
            password_hash = ?,
            last_updated = ?
            WHERE id = 1
            """
        )

        update_pass_query.addBindValue(password_hash)
        update_pass_query.addBindValue(
            datetime.datetime.now().replace(microsecond=0)
        )

        return update_pass_query.exec()

    def set_credentials(
        self,
        server_ip_addr: str,
        server_port: int,
        client_name: str,
        client_token: str
    ) -> bool:
        set_credential_query = QSqlQuery(self.con)

        set_credential_query.prepare(
            """
            INSERT INTO connection_credential (
                server_ip_addr,
                server_port,
                client_name,
                client_token
            ) VALUES (?, ?, ?, ?)
            """
        )

        set_credential_query.addBindValue(server_ip_addr)
        set_credential_query.addBindValue(server_port)
        set_credential_query.addBindValue(client_name)
        set_credential_query.addBindValue(client_token)

        return set_credential_query.exec()

    def get_credentials(self):
        get_credential_query = QSqlQuery(self.con)

        get_credential_query.prepare(
            """
            SELECT
            server_ip_addr,
            server_port,
            client_name,
            client_token
            FROM connection_credential
            """
        )

        get_credential_query.exec()

        if get_credential_query.first():
            data = {
                'server_ip_addr': get_credential_query.value(0),
                'server_port': get_credential_query.value(1),
                'client_name': get_credential_query.value(2),
                'client_token': get_credential_query.value(3)
            }
            return data

        return None

    def update_credentials(
        self,
        server_ip_addr: str,
        server_port: int,
        client_name: str,
        client_token: str
    ) -> bool:
        update_credentials_query = QSqlQuery(self.con)

        if not self.get_credentials():
            return self.set_credentials(
                server_ip_addr,
                server_port,
                client_name,
                client_token
            )

        update_credentials_query.prepare(
            """
            UPDATE connection_credential SET
            server_ip_addr = ?,
            server_port = ?,
            client_name = ?,
            client_token = ?
            WHERE id = 1
            """
        )

        update_credentials_query.addBindValue(server_ip_addr)
        update_credentials_query.addBindValue(server_port)
        update_credentials_query.addBindValue(client_name)
        update_credentials_query.addBindValue(client_token)

        return update_credentials_query.exec()

    def insert_log(self, session_id, details):
        insert_log_query = QSqlQuery(self.con)

        insert_log_query.prepare(
            """
            INSERT INTO log (
                session_id, details, timestamp
            ) VALUES (?, ?, ?)
            """
        )

        insert_log_query.addBindValue(session_id)
        insert_log_query.addBindValue(details)
        insert_log_query.addBindValue(
            datetime.datetime.now().replace(microsecond=0)
        )

        return insert_log_query.exec()

    # def get_all_logs(self):
    #     get_log_query = QSqlQuery(self.con)

    #     get_log_query.prepare(
    #         """
    #         SELECT session_id, logfile_name, timestamp
    #         FROM log
    #         """
    #     )

    #     if get_log_query.first():
    #         return get_log_query

    #     return None

