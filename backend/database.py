import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def _open_connection():

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "4000")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv(
            "DB_NAME",
            "employee_intelligence_system"
        ),

        # TiDB Cloud TLS
        ssl_ca=os.getenv("DB_SSL_CA"),
        ssl_verify_cert=True,
        ssl_verify_identity=True,
    )


class _ReconnectingConnection:
    

    def __init__(self):
        self._conn = None
        self._connect()

    def _connect(self):
        self._conn = _open_connection()

    def _ensure_connected(self):

        try:
            if self._conn is None or not self._conn.is_connected():
                self._connect()
            else:
                # Re-establishes the session if TiDB closed it
                # due to an idle timeout or connection limit.
                self._conn.ping(reconnect=True, attempts=3, delay=1)

        except mysql.connector.Error:
            self._connect()

    def cursor(self, *args, **kwargs):
        self._ensure_connected()
        return self._conn.cursor(*args, **kwargs)

    def commit(self):
        self._ensure_connected()
        return self._conn.commit()

    def rollback(self):
        self._ensure_connected()
        return self._conn.rollback()

    def is_connected(self):
        return self._conn is not None and self._conn.is_connected()


try:

    connection = _ReconnectingConnection()

    print("TiDB Database Connected Successfully")

except mysql.connector.Error as e:

    print("Database Connection Error:", e)

    connection = None