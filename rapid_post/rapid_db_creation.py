"""class functionality to create test database for api testing"""
import psycopg2


class RapidDB:
    def __init__(self, db_credentials) -> None:
        self.db_credentials = db_credentials
        self.rapid_db_connect = self._rapid_db_connect
        self._rapid_payload_analyzer()

    @property
    def _rapid_db_connect(self):
        """functionality to create the connection to the Postgres Database"""
        try:
            rapid_connect = psycopg2.connect(
                database="rapid_db",
                user="root",
                password="root",
                host="localhost",
                port="5432",
            )
        except Exception as error:
            print(error, "::error")
        return rapid_connect

    def _rapid_payload_analyzer(self):
        """functioanlity to analyze the payload and extract the data to create the database"""
        payload = self.db_credentials
        payload_keys = []
        payload_values = []
        for keys, values in payload.items():
            payload_keys.append(keys)
            if isinstance(values, (str, float, int, bool)):
                type_dict = {"value": values, "type": type(values).__name__}
                payload_values.append(type_dict)
        print(payload_values, "::payload values")

    def _rapid_db_create(self):
        """functionality to create the database based on the Payload data"""
        conn = self.rapid_db_connect
        cursor = conn.cursor()
