"""class functionality to update data in the RapidDB using both PUT and PATCH"""
import json

import psycopg2


class RapidUpdate:
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
        """functionality to update"""
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
