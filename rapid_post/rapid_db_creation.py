"""class functionality to create test database for api testing"""
import psycopg2


class RapidDB:
    def __init__(self, db_credentials) -> None:
        self.db_credentials = db_credentials
        self.rapid_db_connect = self._rapid_db_connect
        create_query = self._rapid_payload_analyzer()
        self._rapid_db_create(create_query)
        self._rapid_db_insert()

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
        create_table_query = (
            "CREATE TABLE TEST (id SERIAL PRIMARY KEY,"
            if "id" not in payload_keys
            else "CREATE TABLE TEST (id INTEGER PRIMARY KEY,"
        )
        create_table_query += ", ".join(
            [f"{column} {datatype['type']}" for column, datatype in zip(payload_keys, payload_values)],
        )
        create_table_query += ")"
        return create_table_query

    def _rapid_db_create(self, query):
        """functionality to create the database based on the Payload data"""
        conn = self.rapid_db_connect
        cursor = conn.cursor()
        try:
            cursor.execute(query)
            conn.commit()
            print("Successfully created Table")
        except Exception as error:
            print("Failed to create Table > ", str(error))

    def _rapid_db_insert(self):
        """functionality to insert data into the table that has been created in the _rapid_db_create function"""
        conn = self.rapid_db_connect
        cursor = conn.cursor()
        payload = self.db_credentials
        payload_keys = []
        payload_values = []
        for keys, values in payload.items():
            payload_keys.append(keys)
            payload_values.append(values)
        insert_into_table_query = f"INSERT INTO TEST ("
        insert_value_query = f" VALUES ("
        for column, value in zip(payload_keys, payload_values):
            insert_into_table_query += f"{column},"
            if isinstance(value, str):
                insert_value_query += f"'{value}',"
            else:
                insert_value_query += f"{str(value)},"
        insert_into_table_query = insert_into_table_query.rstrip(",") + ")"
        insert_value_query = insert_value_query.rstrip(",") + ")"
        insert_query = insert_into_table_query + insert_value_query
        try:
            cursor.execute(insert_query)
            conn.commit()
            conn.close()
            print("Data has been successfully inserted into the table")

        except Exception as error:
            print(f"Failed to insert data into the table {str(error)}")
