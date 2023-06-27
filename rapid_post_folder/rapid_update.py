"""class functionality to update data in the RapidDB using both PUT and PATCH"""
import json

import psycopg2


class RapidUpdate:
    """
    Class for rapidly updating data in a database table.

    Parameters:
    -----------
    id : int
        The ID of the data row to be updated.
    table_name : str
        The name of the database table where the update will be performed.
    payload : dict
        A dictionary containing the new data to be updated.
    method : str
        The type of update operation to be performed (e.g., "UPDATE", "INSERT", "DELETE").

    Usage:
    ------
    rapid_update = RapidUpdate({"id":1}, table_name={"table_name":"my_table"}, payload={"name": "John"}, method="PATCH")
    """

    def __init__(self, id, table_name, payload, method):
        self.id = id
        self.payload = payload
        self.table_name = table_name
        self.method = method
        self.rapid_db_connect = self._rapid_db_connect
        self._rapid_data_update()

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

    def _rapid_data_update(self):
        """Updates data in the table using provided payload and ID.

        If the method is `PUT`, all columns must be provided in the payload.
        Otherwise, only specified columns will be updated.
        The function executes the update query and prints the updated row in JSON format.

        Raises:
            Exception: If any error occurs during database operations.
        """
        conn = self._rapid_db_connect
        cursor = conn.cursor()

        if self.method == "PUT":
            query = f"SELECT * FROM {self.table_name.get('table_name')}"
            cursor.execute(query)
            columns = [column[0] for column in cursor.description]
            payload_key_list = list(self.payload.keys())
            if len(columns) == len(payload_key_list):
                try:
                    rapid_update_query = f"UPDATE {self.table_name.get('table_name')} SET "
                    for key, value in self.payload.items():
                        rapid_update_query += f"{key} = '{value}',"
                    rapid_update_query = rapid_update_query.rstrip(",") + f" WHERE id = {self.id.get('id')}"
                    cursor.execute(rapid_update_query)
                    cursor.execute(
                        f"SELECT row_to_json(t) FROM (SELECT * FROM {self.table_name.get('table_name')} WHERE id = {self.id.get('id')}) t",
                    )
                    updated_row = [cursor.fetchone()[0]]
                    updated_row_formatted_indent = json.dumps(updated_row, indent=4)
                    print(updated_row_formatted_indent, "::updated_row")
                    conn.commit()
                except Exception as error:
                    print(
                        f"Failed to update the data into id {self.id.get('id')} : {error}",
                    )
                finally:
                    conn.close()
            else:
                print("Provide all the datas for column for PUT method")
        else:
            try:
                rapid_update_query = f"UPDATE {self.table_name.get('table_name')} SET "
                for key, value in self.payload.items():
                    rapid_update_query += f"{key} = '{value}',"
                rapid_update_query = rapid_update_query.rstrip(",") + f" WHERE id = {self.id.get('id')}"
                cursor.execute(rapid_update_query)
                cursor.execute(
                    f"SELECT row_to_json(t) FROM (SELECT * FROM {self.table_name.get('table_name')} WHERE id = {self.id.get('id')}) t",
                )
                updated_row = [cursor.fetchone()[0]]
                updated_row_formatted_indent = json.dumps(updated_row, indent=4)
                print(updated_row_formatted_indent, "::updated_row")
                conn.commit()
            except Exception as error:
                print(
                    f"Failed to update the data into id {self.id.get('id')} : {error}",
                )
            finally:
                conn.close()
