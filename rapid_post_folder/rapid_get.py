"""functionality to get the data from the RapidDB"""
import json

import psycopg2


class RapidGet:
    """
    Provides functionality to retrieve data from the database per tables.

    Args:
        payload (str): The payload for the database connection.
        filters (bool): Indicates whether filters should be applied or not.
        filter_data (dict): The filter data to be applied.

    Attributes:
        payload (str): The payload for the database connection.
        filters (bool): Indicates whether filters should be applied or not.
        filter_data (dict): The filter data to be applied.
        rapid_db_connect (method): A method for establishing a connection to the Rapid database.

    Methods:
        _get_rapid_data(): Retrieves the data from the database without applying any filters.
        _get_filtered_rapid_data(): Retrieves the data from the database with applied filters.
    """

    def __init__(self, payload, filters, filter_data_payload):
        self.payload = payload
        self.filters = filters
        self.filter_data_payload = filter_data_payload
        self.rapid_db_connect = self._rapid_db_connect
        if not self.filters:
            self._get_rapid_data()
        else:
            self._get_filtered_rapid_data()

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

    def _get_rapid_data(self):
        """
        Retrieves the data from the RapidDB based on the table name.

        Raises:
            Exception: If an error occurs while fetching the data from the database.

        """
        conn = self.rapid_db_connect
        cursor = conn.cursor()
        table_name = self.payload.get("table_name")
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rapid_data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            rapid_data_json = []
            for row in rapid_data:
                rapid_data_json.append(dict(zip(columns, row)))
            json_data = json.dumps(rapid_data_json, indent=4)
            print(json_data, "::json data")
        except Exception as error:
            print(f"Error occured while fetching the data from the database: {error}")
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def _filter_data(filter_query: str, cursor):
        """functionality to filter data based on the user input"""
        try:
            cursor.execute(filter_query)
            rapid_data = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            rapid_data_json = []
            for row in rapid_data:
                rapid_data_json.append(dict(zip(columns, row)))
            json_data = json.dumps(rapid_data_json, indent=4)
            print(json_data, "::json data")

        except Exception as error:
            print(f"Failed to filter the data as expected : {error}")

    def _get_filtered_rapid_data(self):
        """
        Retrieves the data from the RapidDB based on the table name and the data that
        is to be filtered based on the user requirement.

        Raises:
            Exception: If an error occurs while fetching the data from the database.

        """
        conn = self.rapid_db_connect
        cursor = conn.cursor()
        table_name = self.payload.get("table_name")
        if self.filter_data_payload == {}:
            filter_query = f"SELECT * FROM {table_name}"

        else:
            filter_query = f"SELECT * FROM {table_name} WHERE {self.filter_data_payload.get('filter','')}"
        with self.rapid_db_connect as conn, conn.cursor() as cursor:
            RapidGet._filter_data(filter_query, cursor)
