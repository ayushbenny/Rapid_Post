"""class functionality to create test database for api testing"""
import psycopg2


class RapidDB:
    """
    A class for handling database operations using RapidDB.

    Args:
        db_credentials (dict): A dictionary containing the database connection credentials.

    Attributes:
        db_credentials (dict): The database connection credentials.
        rapid_db_connect (RapidDBConnect): An instance of the RapidDBConnect class for database connection.
    """

    def __init__(self, db_credentials) -> None:
        """
        Initializes a RapidDB object.

        Args:
            db_credentials (dict): A dictionary containing the database connection credentials.
        """
        self.db_credentials = db_credentials
        self.rapid_db_connect = self._rapid_db_connect
        create_query = self._rapid_payload_analyzer()
        self._rapid_db_create(create_query)
        self._rapid_db_insert()

    @property
    def _rapid_db_connect(self):
        """
        Creates a connection to the Postgres Database.

        Returns:
            psycopg2.extensions.connection: The database connection object.

        Raises:
            Exception: If an error occurs while connecting to the database.
        """
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
        """
        Analyzes the payload and extracts the data to create the database table.

        Returns:
            str: The create table query generated from the payload.

        Note:
            The payload should be a dictionary where the keys represent the column names
            and the values represent the corresponding data types.

        Raises:
            None.
        """
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
        """
        Executes the query to create the database table based on the payload data.

        Args:
            query (str): The SQL query to create the table.

        Returns:
            None

        Raises:
            None
        """
        conn = self.rapid_db_connect
        cursor = conn.cursor()
        table_name = query.split(" ")[2]
        try:
            cursor.execute(
                f"SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name.lower()}')",
            )
            exists = cursor.fetchone()[0]
            if exists:
                print(f"Table '{table_name}' already exists in the database.")
            else:
                cursor.execute(query)
                conn.commit()
                print("Successfully created Table")
        except Exception as error:
            print("Failed to create Table > ", str(error))

    def _rapid_db_insert(self):
        """
        Inserts data into the table that has been created in the `_rapid_db_create` function.

        Returns:
            None

        Raises:
            None
        """
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
