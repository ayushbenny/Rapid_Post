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
            type_mapping = {
                str: "VARCHAR(255)",
                int: "INTEGER",
                float: "FLOAT",
                bool: "BOOLEAN",
            }
            if isinstance(values, (str, float, int, bool)):
                type_dict = {"value": values, "type": type_mapping[type(values)]}
                payload_values.append(type_dict)
        create_table_query = f"CREATE TABLE TEST ("
        for column, datatype in zip(payload_keys, payload_values):
            data_type = datatype["type"]
            create_table_query += f"{column} {data_type},"
        create_table_query = create_table_query.rstrip(", ")
        create_table_query += ")"
        return create_table_query

    def _rapid_db_create(self):
        """functionality to create the database based on the Payload data"""
        conn = self.rapid_db_connect
        db_query = self._rapid_payload_analyzer()
        print(db_query, ":::db query")
        cursor = conn.cursor()
